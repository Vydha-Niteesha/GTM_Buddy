import json
import re
import pandas as pd
import spacy
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

class EntityExtractor:
    def __init__(self, domain_knowledge_path='domain_knowledge.json'):
        # Load domain knowledge
        with open(domain_knowledge_path, 'r') as f:
            self.domain_knowledge = json.load(f)
        
        # Load pre-trained NER model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Prepare classification model
        self.prepare_classification_model()
    
    def prepare_classification_model(self):
        # Load dataset
        df = pd.read_csv("calls_dataset.csv")
        
        # Find text column dynamically
        text_column = [col for col in df.columns if 'text' in col.lower()][0]
        
        # Prepare multi-label binarizer
        self.mlb = MultiLabelBinarizer()
        
        # Split labels
        labels = df['labels'].str.split(', ')
        y = self.mlb.fit_transform(labels)
        
        # TF-IDF Vectorization
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        X = self.tfidf_vectorizer.fit_transform(df[text_column])
        
        # Train a classifier
        self.classifier = RandomForestClassifier(random_state=42)
        self.classifier.fit(X, y)
    
    def dictionary_lookup(self, text):
        """Extract entities using dictionary lookup"""
        entities = {}
        
        # Check against domain knowledge
        for category, keywords in self.domain_knowledge.items():
            matched_keywords = [
                keyword for keyword in keywords 
                if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text.lower())
            ]
            if matched_keywords:
                entities[category] = matched_keywords
        
        return entities
    
    def spacy_ner(self, text):
        """Extract entities using SpaCy NER"""
        doc = self.nlp(text)
        ner_entities = {
            'persons': [ent.text for ent in doc.ents if ent.label_ == 'PERSON'],
            'organizations': [ent.text for ent in doc.ents if ent.label_ == 'ORG'],
            'locations': [ent.text for ent in doc.ents if ent.label_ == 'GPE']
        }
        return ner_entities
    
    def classify_snippet(self, text):
        """Classify text snippet"""
        # Vectorize input text
        X_input = self.tfidf_vectorizer.transform([text])
        
        # Predict labels
        y_pred = self.classifier.predict(X_input)
        
        # Convert to label names
        predicted_labels = self.mlb.inverse_transform(y_pred)[0]
        
        return predicted_labels
    
    def generate_summary(self, text):
        """Generate a simple extractive summary"""
        sentences = re.split(r'[.!?]', text)
        return '. '.join(sentences[:2]) + '.'

def create_app():
    app = Flask(__name__)
    extractor = EntityExtractor()
    
    @app.route('/analyze', methods=['POST'])
    def analyze_snippet():
        data = request.json
        text = data.get('text', '')
        
        # Perform analysis
        dictionary_entities = extractor.dictionary_lookup(text)
        spacy_entities = extractor.spacy_ner(text)
        labels = extractor.classify_snippet(text)
        summary = extractor.generate_summary(text)
        
        return jsonify({
            'dictionary_entities': dictionary_entities,
            'spacy_entities': spacy_entities,
            'predicted_labels': labels,
            'summary': summary
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)