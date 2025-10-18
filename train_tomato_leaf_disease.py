from tensorflow import data
from keras import models, layers
from keras.applications import MobileNetV3Large
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.utils import image_dataset_from_directory

TRAIN_FROM_SCRATCH = False

train_path = "tomato/train"
val_path = "tomato/val"

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

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=data.AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=data.AUTOTUNE)

base_model = None
model: models.Sequential = None

if TRAIN_FROM_SCRATCH:
    base_model = MobileNetV3Large(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet",
    )

    base_model.trainable = True

    for layer in base_model.layers[:-5]:
        layer.trainable = False

    data_augmentation = models.Sequential([
        layers.RandomRotation(factor=0.15 / 360 * 2 * 3.14159), # Convert degrees to radians
        layers.RandomBrightness(factor=(-0.2, 0.0)), # Note: brightness range is inverted in new API
    ])

    model = models.Sequential([
        data_augmentation,
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(512, activation="relu"),
        layers.Dense(256, activation="relu"),
        layers.Dense(128, activation="relu"),
        layers.Dense(num_classes, activation="softmax")
    ])
else:
    model = models.load_model("tomato.keras")

model.compile(
    optimizer=Adam(learning_rate=0.0001),
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

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
    callbacks=[early_stop, checkpoint, reduce_lr],
)

model.save("tomato.keras")
model.save_weights("tomato.weights.h5")