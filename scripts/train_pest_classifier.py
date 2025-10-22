import numpy as np

PEST_CONFIG: dict[str, any] = {
    # --- Data and File Paths ---
    "TASK_NAME": "pest_classifier",
    "TRAIN_PATH": "datasets/pests_dataset/train",
    "VAL_PATH": "datasets/pests_dataset/valid",
    "MODEL_SAVE_PATH": "models/pest_classifier/pest_classifier_final.keras",
    "WEIGHTS_SAVE_PATH": "models/pest_classifier/pest_classifier_final.weights.h5",
    "MODEL_CHECKPOINT_SAVE_PATH": "models/pest_classifier/pest_classifier_checkpoint.keras",
    
    # --- Hyperparameters ---
    "TRAIN_FROM_SCRATCH": True,
    "IMAGE_SIZE": (224, 224),
    "BATCH_SIZE": 32,
    "LEARNING_RATE": 1e-4,
    "EPOCHS": 5,
    "SEED": 42, # For data shuffling and augmentation
    
    # --- Transfer Learning Configuration ---
    # The number of final layers in the MobileNetV3Large base model to keep UNFROZEN (trainable).
    "UNFROZEN_BASE_LAYERS_COUNT": 5, 
    
    # --- Class Imbalance Handling ---
    "CLASS_COUNTS": np.array([
        400, # ants
        405, # bees
        331, # beetle
        329, # caterpillar
        246, # earthworms
        390, # earwig
        390, # grasshopper
        397, # moth
        316, # slug
        405, # snail
        392, # wasp,
        394, # weevil
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