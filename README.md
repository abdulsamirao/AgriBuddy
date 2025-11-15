# 🌾 AgriBuddy - Your AI Assistant for Smart Farming

# Introduction

Agriculture plays a vital role in the economy of many countries, including Pakistan, where a significant portion of the population depends on farming. Crop production is often affected by plant leaf diseases and agricultural pests, which can reduce yield and quality. Traditionally, identifying these issues requires expert knowledge and manual inspection, methods that are time-consuming, subjective, and not always accessible to small-scale farmers.

This project aims to build a machine-learning–based image classification system capable of detecting plant leaf diseases and agricultural pests. A user-friendly graphical user interface (GUI) enables easy interaction, making the system accessible to general users.

# Objectives

- Build an image classifier to detect plant leaf diseases.
- Develop individual specialized classifier models for each plant species.
- Create a dedicated classifier for identifying agricultural pests.
- Design a simple GUI for uploading images and viewing predictions.
- Implement a basic authentication system using SQLite.

# Tools and Technologies

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| ML Framework | Keras (TensorFlow) |
| Base Model | MobileNetV3Large |
| Background Augmentation | Pillow, rembg |
| Dataset Source | Kaggle |
| GUI Framework | CustomTkinter |
| Database | SQLite3 |
| Project Management | Trello |

# Features

- Login screen  
- Sign-up screen  
- Home screen  
- Tomato leaf disease classifier  
- Mango leaf disease classifier  
- Cotton leaf disease classifier  
- Agricultural pest classifier  

# Implementation

## Project Management

The project was organized using a Kanban workflow in Trello with five lists:

- Project Backlog  
- Current Focus  
- Doing  
- Review / Testing  
- Done  

All tasks were placed in the Project Backlog and gradually moved through each stage. The *Current Focus* list was limited to 3–4 tasks to maintain efficiency.

## Model Training

A unified training pipeline was created for all four classification models, utilizing transfer learning with MobileNetV3Large and custom classification layers.

### Model Architecture

#### a. Data Augmentation
- RandomFlip (horizontal & vertical)  
- RandomRotation (±10%)  
- RandomBrightness (−20% to +20%)  
- RandomZoom (zoom-out up to 20%)  

#### b. Base Model
- MobileNetV3Large used for feature extraction  
- Initially frozen during Phase 1  

#### c. Classification Head
- GlobalAveragePooling2D  
- Dense(512) + ReLU  
- BatchNormalization  
- Dense(256) + ReLU + Dropout(0.3)  
- Softmax output layer  

### Training Process

#### Phase 1: Base Frozen
- Only classification head trained  
- Higher learning rate (1e-3)  
- Achieved ~80% validation accuracy  

#### Phase 2: Fine-Tuning
- Last 5 layers unfrozen  
- Learning rate reduced (1e-4)  
- Validation accuracy exceeded 90%  

#### Callbacks Used
- ReduceLROnPlateau  
- EarlyStopping  
- ModelCheckpoint  

### Training Framework

A modular system was built using a ClassifierTrainer base class:

- Handles data loading, model creation, compilation, and training  
- Individual trainer files import the base class and pass custom configurations  

Configurations included:

- Dataset paths  
- Model save paths  
- Hyperparameters  
- Image size  
- Class counts for imbalance handling  
- Number of unfrozen base layers  

### Dataset Preparation & Balancing

#### Dataset Splitting
Some datasets were split into train/validation using `splitfolders`.

#### Class Weighting
- A script counted images per class  
- Weights computed using inverse frequency normalization  
- Ensured minority classes received higher gradient importance  

### Background Augmentation (Mango Dataset)

The mango dataset contained images with plain white backgrounds, limiting generalization.

To improve performance:

1. Used Pillow + rembg for background removal.  
2. Created a folder of natural backgrounds.  
3. Combined segmented leaves with random real backgrounds.  
4. Used ProcessPoolExecutor for parallel processing.

This significantly improved dataset diversity and model generalization.

## User Interface

The GUI was built using CustomTkinter, structured across multiple pages, each implemented as a class inheriting from `CTkFrame`.

### Pages Implemented

- LoginPage  
- SignUpPage  
- HomePage  
- TomatoLeafDiseasePage  
- MangoLeafDiseasePage  
- CottonLeafDiseasePage  
- PestClassificationPage  

Navigation is handled by raising frames through a controller.

### Login & Sign-Up Pages

Components used:
- `CTkLabel`
- `CTkEntry`
- `CTkButton`
- Message labels for errors/success

Authentication logic:
- Local SQLite database  
- Validation inside page classes  
- Database interactions handled via `database.py`

## Home Page

The Home Page provides buttons to navigate to:

- Tomato Disease Detection  
- Mango Disease Detection  
- Cotton Disease Detection  
- Pest Detection  

## Model Pages

All model pages inherit from a shared class BaseModelPage containing:

- Back button  
- Select Image button  
- Drag-and-drop support  
- Image preview  
- Process button  
- Output textbox  

This prevents code duplication.

# Conclusion

This project successfully developed a high-accuracy leaf disease and pest classification system with a modern GUI. Using transfer learning, background augmentation, class balancing, and modular training scripts, the system achieved over 90% validation accuracy across all models.

The project demonstrates how deep learning can effectively address real agricultural challenges.

# Future Work

### 1. Image Segmentation
Use segmentation models to remove background noise and isolate the leaf.

### 2. Hierarchical Classification
Merge similar diseases into broader categories and use secondary models for fine-grained classification.

### 3. Cloud Deployment
Move models to the cloud, allowing:
- Device-independent usage  
- More secure model storage  
- Monetization through rate limits / API credits  

### 4. Web Application
Develop a browser-based version accessible from any device.

### 5. Full Backend for Authentication
Implement:
- User accounts  
- Secure login/registration  
- Prediction history  
- Admin controls  
- Free/paid tiers  

# Overall Outlook

With further enhancements in preprocessing, dataset design, cloud deployment, and backend integration, AgriBuddy has the potential to evolve into a commercial-grade, scalable, and widely adopted agricultural assistant.

---

Icon credits:
https://www.flaticon.com/free-icons/sprout