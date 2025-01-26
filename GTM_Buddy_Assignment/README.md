
# Entity Extractor and Text Classification API

## Overview
This project involves the development of a text analysis tool that classifies text snippets, extracts domain-specific entities, and generates summaries. It includes a RESTful API built using Flask, where users can send text data to analyze using various techniques such as dictionary lookup, SpaCy Named Entity Recognition (NER), and machine learning classification. The model is trained on a dataset of labeled text snippets to predict categories like "pricing discussion," "security," "features," etc.

## Features
- **Entity Extraction**: Extract entities using:
  - **Dictionary Lookup**: Matches text against domain-specific keywords (e.g., competitors, features).
  - **SpaCy NER**: Identifies named entities such as persons, organizations, and locations.
- **Text Classification**: Classifies text into multiple categories based on trained machine learning models (Random Forest classifier).
- **Text Summarization**: Generates a simple extractive summary of the input text.

## Components
- **EntityExtractor Class**: Handles entity extraction, text classification, and summary generation.
- **Flask API**: Exposes a REST API for analyzing text snippets.
- **Dataset Generation**: A Python script to generate the dataset for training and testing.

## Files
1. **`generate_dataset.py`**: Generates the synthetic dataset used for training.
2. **`main.py`**: Implements the Flask API and the logic for text classification, entity extraction, and summarization.
3. **`domain_knowledge.json`**: Contains domain-specific knowledge, such as competitor names and relevant keywords, used for entity extraction.

## Prerequisites
- Python 3.6+
- Install required libraries via `pip`:
  ```bash
  pip install flask pandas spacy scikit-learn
  python -m spacy download en_core_web_sm
  ```

## Usage
1. **Generate Dataset**:
   - Run the `generate_dataset.py` script to create a sample dataset (`calls_dataset.csv`).
   ```bash
   python generate_dataset.py
   ```

2. **Run the Flask API**:
   - Start the Flask server by running `main.py`:
   ```bash
   python main.py
   ```
   The server will run on `http://localhost:5000`.

3. **API Endpoint**:
   - **POST /analyze**:
     - **Request body** (JSON):
       ```json
       {
         "text": "We love the analytics, but CompetitorX has a cheaper subscription."
       }
       ```
     - **Response body** (JSON):
       ```json
       {
         "dictionary_entities": {
           "competitors": ["CompetitorX"],
           "features": ["analytics"]
         },
         "spacy_entities": {
           "persons": [],
           "organizations": [],
           "locations": []
         },
         "predicted_labels": ["Pricing Discussion", "Features"],
         "summary": "We love the analytics, but CompetitorX has a cheaper subscription."
       }
       ```
     - The API returns:
       - **dictionary_entities**: Matched domain-specific keywords.
       - **spacy_entities**: Named entities detected using SpaCy (persons, organizations, locations).
       - **predicted_labels**: Text snippet classification labels.
       - **summary**: Extractive summary of the text.

## How it Works
1. **Dataset Generation**:
   - The `generate_dataset.py` script creates a dataset with labeled text snippets. It repeats and extends a smaller set of example texts to generate 120 samples.

2. **Entity Extraction**:
   - The **dictionary lookup** searches for keywords in the text based on a predefined set of domain-specific categories like competitors, features, and pricing.
   - The **SpaCy NER** extracts persons, organizations, and locations from the text.

3. **Text Classification**:
   - The **Random Forest classifier** is trained on the dataset of labeled text snippets. It predicts the categories based on the content of the text using TF-IDF vectorization.

4. **Text Summarization**:
   - A simple extractive summarization approach is used to create a summary by selecting the first few sentences.

## Example
Here is an example of an API call:

```bash
curl -X POST http://localhost:5000/analyze -H "Content-Type: application/json" -d '{"text": "We love the analytics, but CompetitorX has a cheaper subscription."}'
```

### Response:
```json
{
  "dictionary_entities": {
    "competitors": ["CompetitorX"],
    "features": ["analytics"]
  },
  "spacy_entities": {
    "persons": [],
    "organizations": [],
    "locations": []
  },
  "predicted_labels": ["Pricing Discussion", "Features"],
  "summary": "We love the analytics, but CompetitorX has a cheaper subscription."
}
```


