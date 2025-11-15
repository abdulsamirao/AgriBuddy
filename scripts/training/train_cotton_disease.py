import numpy as np

CONFIG: dict[str, any] = {
    # Data and File Paths
    "TASK_NAME": "cotton_disease_classifier",
    "TRAIN_PATH": "datasets/cotton_disease_dataset/train",
    "VAL_PATH": "datasets/cotton_disease_dataset/val",
    "MODEL_SAVE_PATH": "models/cotton_disease_classifier/cotton_disease_classifier_final.keras",
    "WEIGHTS_SAVE_PATH": "models/cotton_disease_classifier/cotton_disease_classifier_final.weights.h5",
    "MODEL_CHECKPOINT_SAVE_PATH": "models/cotton_disease_classifier/cotton_disease_classifier_checkpoint.keras",
    
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
        200,  # Bacterial Blight
        344,  # Curl Virus
        205,  # Healthy Leaf
        221,  # Herbicide Growth Damage
        180,  # Leaf Hopper Jassids
        462,  # Leaf Redding
        92,   # Leaf Variegation
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