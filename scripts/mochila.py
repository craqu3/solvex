
from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import time
import board
import adafruit_dht
import random


import pymysql


def get_db_connection():
    return pymysql.connect(
        host="shinkansen.proxy.rlwy.net",
        user="root",
        password="cNUrAARLAswDhQvRhetaUXwWkIjOMoCC",
        database="railway",
        port=54714,
        cursorclass=pymysql.cursors.DictCursor
    )

conn = get_db_connection()
cursor = conn.cursor()

'''
status = 1
temperature_c = 31.5
senha_atual = 8745
res_code = senha_atual
humidity = 5.0

cursor.execute(
                "INSERT INTO bag (status, temperature, user_code, res_code, humidity) VALUES (%s, %s, %s, %s, %s)",
                (status, temperature_c, senha_atual, res_code, humidity)
)   
conn.commit()
cursor.close()
conn.close()

'''


'''
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


sensor = adafruit_dht.DHT22(board.D4)


senha_atual = ""
proxima_troca = datetime.now() + timedelta(minutes=5)

entrada = []

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
    GPIO.cleanup()

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


try:
    senha_atual = gerar_nova_senha()
    print("🔐 Nova senha gerada:", senha_atual)

    while True:
        try:

            temperature_c = sensor.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = sensor.humidity
            print(f"🌡 Temp={temperature_c:.1f}ºC, Humidity={humidity:.1f}%")

        except RuntimeError as error:
            print("Erro de leitura:", error.args[0])
        except Exception as error:
            sensor.exit()
            raise error


        agora = datetime.now()
        status = 1
        if agora >= proxima_troca:
            senha_atual = gerar_nova_senha()
            cursor.execute(
                "INSERT INTO bag (status, temperature, user_code, humidity) VALUES (%s, %s, %s, %s)",
                (status, temperature_c, senha_atual, humidity)
            )   
        conn.commit()
        proxima_troca = agora + timedelta(minutes=5)
        print("🔐 Nova senha gerada:", senha_atual)


        time.sleep(3)

except KeyboardInterrupt:
    print("\nPrograma terminado com CTRL+C.")
    sensor.exit()
    GPIO.cleanup()

'''
