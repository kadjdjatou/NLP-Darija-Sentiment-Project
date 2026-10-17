# NLP Darija Sentiment Analysis

Sentiment analysis project on Moroccan Darija comments collected from social media, with a comparison of classical Machine Learning and Transformer-based approaches.

## Project Overview

The objective of this project is to classify Moroccan Darija comments according to their sentiment.

The project focuses on a challenging NLP setting due to:
- the informal nature of Moroccan Darija,
- spelling variations,
- code-switching,
- the coexistence of Arabic and Latin scripts,
- and the limited availability of high-quality labeled datasets.

The study compares several text representation and classification approaches, from traditional machine learning pipelines to pretrained Transformer models.

## Dataset

The dataset was built from public social media comments, mainly collected from YouTube.

Main characteristics:
- around **130,000 raw comments** collected,
- **83,411 comments** selected and annotated for the study,
- a manually labeled reference subset of **1,600 comments** created with Label Studio,
- semi-assisted annotation using Gemini followed by human correction.

The dataset was cleaned and prepared before training through several preprocessing steps adapted to Darija text.

## Approaches

More than 25 model / representation combinations were explored.

### Classical Machine Learning

Text representations:
- Bag of Words
- TF-IDF

Models:
- Logistic Regression
- Support Vector Machine
- Naive Bayes
- Stacking classifiers

### Deep Learning / Transformers

Several pretrained language models were evaluated, including:
- BERTDarija
- AraBERT

These models were fine-tuned and compared with traditional machine learning approaches.

## Experiment Tracking

Experiments were monitored using:

- MLflow
- Weights & Biases

These tools were used to compare models, metrics and training configurations.

## Results

Best results obtained during the project:

| Approach | F1-score |
|---|---:|
| BERTDarija | **0.743** |
| Stacking model | **0.730** |

BERTDarija achieved the best overall performance among the evaluated approaches.

## Project Workflow

```text
Data Collection
      ↓
Data Cleaning
      ↓
Manual / Assisted Annotation
      ↓
Text Representation
      ↓
Model Training
      ↓
Experiment Tracking
      ↓
Model Evaluation
      ↓
Comparison of Approaches
