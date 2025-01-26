import pandas as pd
import random

def generate_dataset():
    text_snippets = [
        "We love the analytics, but CompetitorX has a cheaper subscription.",
        "Our compliance team is worried about data handling. Are you SOC2 certified?",
        "Do you offer any discounts for enterprise customers?",
        "I am concerned about data security and GDPR compliance.",
        "CompetitorY is offering a similar solution at a lower cost.",
        "Your AI engine looks impressive, but the pricing model is unclear.",
        "How does your data pipeline compare with industry standards?",
        "We need advanced analytics for our sales team.",
        "Can you explain your renewal cost structure?",
        "Interested in understanding your budget-friendly options.",
        "CompetitorZ seems to have more flexible pricing.",
        "I want to evaluate your AI engine's capabilities.",
        "What makes your data pipeline unique?",
        "Looking for a cost-effective analytics solution.",
        "How competitive are your pricing models?"
    ]

    labels_list = [
        ["Positive", "Pricing Discussion", "Features"],
        ["Security", "Compliance"],
        ["Pricing Discussion", "Budget"],
        ["Security", "Compliance"],
        ["Competition", "Pricing Discussion"],
        ["Features", "Pricing Discussion"],
        ["Technical Capabilities"],
        ["Features", "Positive"],
        ["Pricing Discussion"],
        ["Budget", "Pricing Discussion"],
        ["Competition", "Pricing Discussion"],
        ["Features", "Technical Evaluation"],
        ["Technical Capabilities"],
        ["Budget", "Pricing Discussion"],
        ["Competition", "Pricing Discussion"]
    ]

    # Ensure labels match text snippets
    final_labels = labels_list

    # Generate 120 samples by repeating or sampling the original list
    text_snippets_extended = random.choices(text_snippets, k=120)
    labels_extended = random.choices(final_labels, k=120)

    # Generate dataset
    data = {
        "id": list(range(1, 121)),
        "cleaned_text": text_snippets_extended,
        "labels": [", ".join(labels) for labels in labels_extended]
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv("calls_dataset.csv", index=False)
    
    print("Dataset generated successfully:")
    print(df.head())  # Print first few rows to check
    
    return df

if __name__ == "__main__":
    generate_dataset()