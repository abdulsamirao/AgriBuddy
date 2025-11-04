import numpy as np

PEST_CONFIG: dict[str, any] = {
    # --- Data and File Paths ---
    "TASK_NAME": "wheat_disease_classifier",
    "TRAIN_PATH": "datasets/wheat_disease_dataset/train",
    "VAL_PATH": "datasets/wheat_disease_dataset/valid",
    "MODEL_SAVE_PATH": "models/wheat_disease_classifier/wheat_disease_classifier_final.keras",
    "WEIGHTS_SAVE_PATH": "models/wheat_disease_classifier/wheat_disease_classifier_final.weights.h5",
    "MODEL_CHECKPOINT_SAVE_PATH": "models/wheat_disease_classifier/wheat_disease_classifier_checkpoint.keras",
    
    # --- Hyperparameters ---
    "TRAIN_FROM_SCRATCH": False,
    "IMAGE_SIZE": (224, 224),
    "BATCH_SIZE": 32,
    "LEARNING_RATE": 1e-4,
    "EPOCHS": 30,
    "SEED": 42, # For data shuffling and augmentation
    
    # --- Transfer Learning Configuration ---
    # The number of final layers in the MobileNetV3Large base model to keep UNFROZEN (trainable).
    "UNFROZEN_BASE_LAYERS_COUNT": 5, 
    
    # --- Class Imbalance Handling ---
    "CLASS_COUNTS": np.array([
        903,   # Aphid
        576,   # Black Rust
        647,   # Blast
        1271,  # Brown Rust
        614,   # Common Root Rot
        611,   # Fusarium Head Blight
        1000,  # Healthy
        842,   # Leaf Blight
        1081,  # Mildew
        800,   # Mite
        1144,  # Septoria
        1310,  # Smut
        234,   # Stem fly
        770,   # Tan spot
        1301   # Yellow Rust
    ]),
}

from classifer_trainer import ClassifierTrainer

if __name__ == "__main__":
    print(f"Starting training for {PEST_CONFIG['TASK_NAME']}...")
    
    trainer = ClassifierTrainer(PEST_CONFIG)
    
    train_ds, val_ds = trainer.load_datasets()
    
    trainer.build_or_load_model()
    
    trainer.compile_model()
    
    trainer.train(train_ds, val_ds)