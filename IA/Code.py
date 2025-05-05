import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import layers
from sklearn.metrics import classification_report, confusion_matrix

# Caminhos dos dados
train_path = r'C:\Users\marco\OneDrive\Documentos\dataset\training'
val_path = r'C:\Users\marco\OneDrive\Documentos\dataset\validation'

# Pré-processamento das imagens
img_height, img_width = 128, 128
batch_size = 32

# Aumento de dados para o conjunto de treinamento
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,  # Rotacionar imagens aleatoriamente
    width_shift_range=0.2,  # Deslocamento horizontal
    height_shift_range=0.2,  # Deslocamento vertical
    shear_range=0.2,  # Cortes aleatórios
    zoom_range=0.2,  # Zoom aleatório
    horizontal_flip=True,  # Flip horizontal
    fill_mode='nearest'  # Preencher pixels ausentes após transformações
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

val_generator = val_datagen.flow_from_directory(
    val_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=False
)

# Carregar o modelo pré-treinado MobileNetV2
base_model = MobileNetV2(input_shape=(img_height, img_width, 3), include_top=False, weights='imagenet')

# Congelar as camadas do modelo base (MobileNetV2)
base_model.trainable = False

# Construção do modelo com MobileNetV2
model = Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),  # Substituindo Flatten por GlobalAveragePooling
    Dense(128, activation='relu'),
    Dropout(0.5),  # Dropout mais alto para prevenir overfitting
    Dense(1, activation='sigmoid')  # Para classificação binária
])

# Compilação do modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Callbacks
early_stop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)
checkpoint = ModelCheckpoint('cnn_best_model_mobilenet.h5', monitor='val_accuracy', save_best_only=True)

# Treinamento do modelo
history = model.fit(
    train_generator,
    epochs=30,
    validation_data=val_generator,
    callbacks=[early_stop, checkpoint]
)

# Avaliação
val_loss, val_accuracy = model.evaluate(val_generator)
print(f"Acurácia no conjunto de validação: {val_accuracy:.4f}")

# Carregar o melhor modelo
best_model = load_model('cnn_best_model_mobilenet.h5')

# Previsões
y_true = val_generator.classes
y_pred = (best_model.predict(val_generator) > 0.5).astype("int32")

# Relatório de classificação
print("\nRelatório de Classificação:")
print(classification_report(y_true, y_pred, target_names=list(val_generator.class_indices.keys())))

# Matriz de confusão
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=val_generator.class_indices.keys(), yticklabels=val_generator.class_indices.keys())
plt.xlabel('Previsão')
plt.ylabel('Real')
plt.title('Matriz de Confusão')
plt.show()
