from tensorflow import data
import numpy as np
from keras import models, layers
from keras.applications import MobileNetV3Large
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.utils import image_dataset_from_directory
import os

class ClassifierTrainer:
    def __init__(self, config: dict[str, any]):
        self.config = config
        self.num_classes = 0
        self.class_weights = {}
        self.model: models.Sequential = None

    def _calculate_class_weights(self) -> dict[int, float]:
        """Calculates class weights inversely proportional to class frequency."""
        counts = self.config["CLASS_COUNTS"]
        total_samples = np.sum(counts)
        num_classes = len(counts)
        
        weights = (total_samples / num_classes) / counts
        weights /= np.mean(weights) 
        
        class_weights = {i: float(weight) for i, weight in enumerate(weights)}
        
        print("\n--- Calculated Class Weights ---")
        for i, weight in class_weights.items():
            print(f"Class {i} (Count: {counts[i]:4d}): Weight = {weight:.3f}")
            
        return class_weights

    def load_datasets(self):
        """Loads and pre-fetches the training and validation datasets."""
        train_ds = image_dataset_from_directory(
            directory=self.config["TRAIN_PATH"],
            labels="inferred",
            label_mode="categorical",
            image_size=self.config["IMAGE_SIZE"],
            batch_size=self.config["BATCH_SIZE"],
            shuffle=True,
            seed=self.config["SEED"],
        )

        val_ds = image_dataset_from_directory(
            directory=self.config["VAL_PATH"],
            labels="inferred",
            label_mode="categorical",
            image_size=self.config["IMAGE_SIZE"],
            batch_size=self.config["BATCH_SIZE"],
            shuffle=True,
            seed=self.config["SEED"],
        )
        
        self.num_classes = len(train_ds.class_names)
        
        print("Train Class Names:")
        print(train_ds.class_names)
        
        print("Validation Class Names:")
        print(val_ds.class_names)
        
        # Calculate class weights now that we know the number of classes
        if self.config["CLASS_COUNTS"] is not None and len(self.config["CLASS_COUNTS"]) == self.num_classes:
             self.class_weights = self._calculate_class_weights()
        else:
            print("\nWARNING: Class counts not provided or mismatched. Training without class weights.")
        
        # Data Optimization
        train_ds = train_ds.prefetch(buffer_size=data.AUTOTUNE)
        val_ds = val_ds.prefetch(buffer_size=data.AUTOTUNE)
        
        return train_ds, val_ds

    def build_or_load_model(self):
        """Builds a new model or loads an existing one for fine-tuning."""
        
        if self.config["TRAIN_FROM_SCRATCH"] or not os.path.exists(self.config["MODEL_SAVE_PATH"]):
            print("\n--- Building Model from Scratch ---")
            
            base_model = MobileNetV3Large(
                input_shape=(*self.config["IMAGE_SIZE"], 3),
                include_top=False,
                weights="imagenet",
            )
            
            base_model.trainable = True

            # Freeze initial layers
            # Can adjust the number of layers to keep unfrozen here
            for layer in base_model.layers[:-self.config["UNFROZEN_BASE_LAYERS_COUNT"]]:
                layer.trainable = False

            # Data Augmentation Layer
            data_augmentation = models.Sequential([
                layers.RandomFlip("horizontal_and_vertical"),
                layers.RandomRotation(factor=0.1),
                layers.RandomBrightness(factor=(-0.2, 0.2)),
                layers.RandomZoom(height_factor=(-0.2, 0.0), width_factor=(-0.2, 0.0)),
            ])

            self.model = models.Sequential([
                layers.Input(shape=(*self.config["IMAGE_SIZE"], 3)),
                data_augmentation,
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.Dense(512, activation="relu"),
                layers.BatchNormalization(),
                layers.Dense(256, activation="relu"),
                layers.Dropout(0.3),
                layers.Dense(self.num_classes, activation="softmax")
            ])
            
        else:
            print(f"\n--- Loading Model for Fine-Tuning: {self.config['MODEL_SAVE_PATH']} ---")
            self.model = models.load_model(self.config["MODEL_SAVE_PATH"])
            
            # Unfreeze top layers for fine-tuning
            base_model = self.model.get_layer("MobileNetV3Large")
            if base_model:
                print("Unfreezing top layers of MobileNetV3Large...")
                base_model.trainable = True
                # Can adjust the number of layers to unfreeze here too
                for layer in base_model.layers[:-self.config["UNFROZEN_BASE_LAYERS_COUNT"]]:
                    layer.trainable = False
            else:
                 print("WARNING: Could not find MobileNetV3Large layer for unfreezing.")


    def compile_model(self):
        """Configures the model for training."""
        self.model.compile(
            optimizer=Adam(learning_rate=self.config["LEARNING_RATE"]),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
        print(self.model.summary())

    def train(self, train_ds, val_ds):
        """Runs the training loop with callbacks."""
        
        # Define Callbacks
        early_stop = EarlyStopping(
            monitor="val_loss", patience=3, restore_best_weights=True,
        )

        checkpoint = ModelCheckpoint(
            self.config["MODEL_CHECKPOINT_SAVE_PATH"],
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
        )

        reduce_lr = ReduceLROnPlateau(
            monitor="val_loss", factor=0.2, patience=2, min_lr=1e-7,
        )

        print(f"\n--- Starting Training for {self.config['EPOCHS']} Epochs ---")
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=self.config["EPOCHS"],
            callbacks=[early_stop, checkpoint, reduce_lr],
            class_weight=self.class_weights if self.class_weights else None,
        )
        
        # Save final model state
        self.model.save(self.config["MODEL_SAVE_PATH"])
        self.model.save_weights(self.config["WEIGHTS_SAVE_PATH"])
        print(f"\nModel and weights saved to {self.config['MODEL_SAVE_PATH']}")
        return history