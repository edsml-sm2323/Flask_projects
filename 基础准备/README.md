# BERT and DeBERTa-v3 Fine-tuning for Multiple Choice Questions
## Requirement:  
Predict the top three most probable answers given the prompt  

## Overview:  
The complete process of fine-tuning a pre-trained BERT model for a multiple-choice task. The process covers all stages from data preprocessing, model configuration, training to prediction

## Implementation steps:
### Step1: Data preprocessing 
Load and transform datasets to prepare data in the appropriate format for training and testing.

### Step2: Model fine-tuning 
Based on the `bert-base-cased` model, multiple-choice questions are trained.

### Step3: Training configuration  
Set training parameters such as batch size, learning rate, weight decay, etc.

### Step4: prediction
Make predictions on the test set and output the best three possible answers to each question.
