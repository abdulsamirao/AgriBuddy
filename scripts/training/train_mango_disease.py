import numpy as np

CONFIG: dict[str, any] = {
    # Data and File Paths
    "TASK_NAME": "mango_disease_classifier",
    "TRAIN_PATH": "datasets/mango_disease_dataset/train",
    "VAL_PATH": "datasets/mango_disease_dataset/val",
    "MODEL_SAVE_PATH": "models/mango_disease_classifier/mango_disease_classifier_final.keras",
    "WEIGHTS_SAVE_PATH": "models/mango_disease_classifier/mango_disease_classifier_final.weights.h5",
    "MODEL_CHECKPOINT_SAVE_PATH": "models/mango_disease_classifier/mango_disease_classifier_checkpoint.keras",
    
    # Hyperparameters
    "TRAIN_FROM_SCRATCH": False,
    "IMAGE_SIZE": (224, 224),
    "BATCH_SIZE": 32,
    "LEARNING_RATE": 4e-6,
    "EPOCHS": 30,
    "SEED": 42, # For data shuffling and augmentation
    
    # Transfer Learning Configuration
    # The number of final layers in the MobileNetV3Large base model to keep UNFROZEN (trainable).
    "UNFROZEN_BASE_LAYERS_COUNT": 5, 
    
    # Class Imbalance Handling
    "CLASS_COUNTS": np.array([
        400,  # Anthracnose
        400,  # Bacterial Canker
        #400,  # Cutting Weevil
        399,  # Die Back
        400,  # Gall Midge
        400,  # Healthy
        400,  # Powdery Mildew
        400,  # Sooty Mould
    ]),
}

from classifer_trainer import ClassifierTrainer

if __name__ == "__main__":
    print(f"Starting training for {CONFIG['TASK_NAME']}...")
    
    trainer = ClassifierTrainer(CONFIG)
    
    train_ds, val_ds = trainer.load_datasets()
    
    trainer.build_or_load_model()
    
    trainer.compile_model()
    
    trainer.train(train_ds, val_ds)