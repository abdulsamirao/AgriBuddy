from tensorflow import data
import numpy as np
from keras import models, layers
from keras.applications import MobileNetV3Large
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.utils import image_dataset_from_directory

TRAIN_FROM_SCRATCH = False
LEARNING_RATE = 2e-5

train_path = "tomato-new/train"
val_path = "tomato-new/valid"

train_ds = image_dataset_from_directory(
    directory=train_path,
    labels="inferred",
    label_mode="categorical",
    image_size=(224, 224),
    batch_size=32,
    shuffle=True,
    seed=123,
)

val_ds = image_dataset_from_directory(
    directory=val_path,
    labels="inferred",
    label_mode="categorical",
    image_size=(224, 224),
    batch_size=32,
    shuffle=True,
    seed=123,
)

num_classes = len(train_ds.class_names)

print("Train Class Names:", train_ds.class_names)
print("Validation Class Names:", val_ds.class_names)

# Temporarily commented out due to issues with cache file
#train_ds = train_ds.cache().prefetch(buffer_size=data.AUTOTUNE)
#val_ds = val_ds.cache().prefetch(buffer_size=data.AUTOTUNE)

base_model = None
model: models.Sequential = None

if TRAIN_FROM_SCRATCH:
    base_model = MobileNetV3Large(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet",
    )

    base_model.trainable = True

    for layer in base_model.layers[:-1]:
        layer.trainable = False

    data_augmentation = models.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(factor=0.1), # Rotates by +/- 36 degrees (0.1 * 2*pi).
        layers.RandomBrightness(factor=(-0.2, 0.2)), 
        layers.RandomZoom(height_factor=(-0.2, 0.0), width_factor=(-0.2, 0.0)), 
    ])

    model = models.Sequential([
        layers.Input(shape=(224, 224, 3)),
        data_augmentation,
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(512, activation="relu"),
        layers.BatchNormalization(),
        layers.Dense(256, activation="relu"),
        layers.Dense(num_classes, activation="softmax")
    ])
else:
    model = models.load_model("tomato.keras")
    base_model = model.get_layer("MobileNetV3Large")
    for layer in base_model.layers[-3:]:
        print(layer.trainable)
        layer.trainable = True
    

model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

print(model.summary())

early_stop = EarlyStopping(
    monitor="val_loss",
    patience = 3,
    restore_best_weights = True,
)

checkpoint = ModelCheckpoint(
    "best_tomato_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.2,
    patience=2,
    min_lr=1e-7,
)

CLASS_COUNTS = np.array([
    2826, # 0. Tomato___Bacterial_Spot
    2455, # 1. Tomato___Early_Blight
    3051, # 2. Tomato___Healthy
    3113, # 3. Tomato___Late_Blight
    2754, # 4. Tomato___Leaf_Mold
    2153, # 5. Tomato___Mosaic_Virus
    1004, # 6. Tomato___Powdery_Mildew
    2882, # 7. Tomato___Septoria_Leaf_Spot
    1747, # 8. Tomato___Spider_Mites_Two-Spotted
    1827, # 9. Tomato___Target_Spot
    2036, # 10. Tomato___Yellow_Leaf_Curl_Virus
])

def calculate_class_weights(counts):
    """Calculates class weights inversely proportional to class frequency."""
    total_samples = np.sum(counts)
    num_classes = len(counts)
    
    # Calculate initial weights
    weights = (total_samples / num_classes) / counts
    
    # Normalize weights so the mean weight is 1 (optional, but good practice)
    weights /= np.mean(weights) 
    
    # Convert to dictionary format required by Keras: {class_index: weight}
    class_weights = {i: weight for i, weight in enumerate(weights)}
    
    print("\n--- Calculated Class Weights ---")
    for i, weight in class_weights.items():
        print(f"Class {i} (Count: {counts[i]:4d}): Weight = {weight:.3f}")
        
    return class_weights

class_weights = calculate_class_weights(CLASS_COUNTS)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=5,
    callbacks=[early_stop, checkpoint, reduce_lr],
    class_weight=class_weights,
)

model.save("tomato.keras")
model.save_weights("tomato.weights.h5")