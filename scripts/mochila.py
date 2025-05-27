from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import time
import board
import adafruit_dht
import random
import pymysql

# --- Conexão com Banco ---
def get_db_connection():
    return pymysql.connect(
        host="shinkansen.proxy.rlwy.net",
        user="root",
        password="cNUrAARLAswDhQvRhetaUXwWkIjOMoCC",
        database="railway",
        port=54714,
        cursorclass=pymysql.cursors.DictCursor
    )

# --- Keypad ---
KEYPAD = [
    ["1","2","3"],
    ["4","5","6"],
    ["7","8","9"],
    ["*","0","#"]
]
ROW_PINS = [4, 17, 27, 22]
COL_PINS = [18, 23, 24]

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# --- Sensor ---
sensor = adafruit_dht.DHT22(board.D4)

# --- Variáveis Globais ---
senha_atual = ""
entrada = []
proxima_troca = datetime.now() + timedelta(minutes=5)

# --- Funções ---
def gerar_nova_senha():
    return str(random.randint(1000, 9999))

def validar_senha(senha_digitada):
    global senha_atual
    if senha_digitada == senha_atual:
        print("✅ Senha correta! Abrindo mochila...")
        acionar_solenoide()
    else:
        print("❌ Senha incorreta.")

def acionar_solenoide():
    SOLENOIDE_PIN = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOLENOIDE_PIN, GPIO.OUT)
    GPIO.output(SOLENOIDE_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(SOLENOIDE_PIN, GPIO.LOW)

def tecla_pressionada(tecla):
    global entrada
    print(f"Tecla: {tecla}")
    if tecla == "#":
        senha_digitada = "".join(entrada)
        validar_senha(senha_digitada)
        entrada = []
    elif tecla == "*":
        entrada = []
        print("Senha limpa")
    else:
        entrada.append(tecla)

keypad.registerKeyPressHandler(tecla_pressionada)

# --- Execução Principal ---
try:
    senha_atual = gerar_nova_senha()
    print("🔐 Nova senha gerada:", senha_atual)

    while True:
        try:
            temperature_c = sensor.temperature
            humidity = sensor.humidity

            if temperature_c is not None and humidity is not None:
                print(f"🌡 Temp={temperature_c:.1f}ºC, Humidade={humidity:.1f}%")
            else:
                print("⚠️ Sensor retornou None, ignorando leitura.")

        except RuntimeError as error:
            print("Erro de leitura do sensor:", error.args[0])
            continue
        except Exception as error:
            print("Erro inesperado:", error)
            continue

        agora = datetime.now()
        if agora >= proxima_troca:
            senha_atual = gerar_nova_senha()
            print("🔐 Nova senha gerada:", senha_atual)

            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                status = 1
                cursor.execute(
                    "INSERT INTO bag (status, temperature, user_code, humidity) VALUES (%s, %s, %s, %s)",
                    (status, temperature_c, senha_atual, humidity)
                )
                conn.commit()
            except Exception as db_error:
                print("Erro ao gravar no banco de dados:", db_error)
            finally:
                cursor.close()
                conn.close()

            proxima_troca = agora + timedelta(minutes=5)

        time.sleep(3)

except KeyboardInterrupt:
    print("\n🛑 Programa terminado com CTRL+C.")
finally:
    sensor.exit()
    GPIO.cleanup()
