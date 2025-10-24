from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def build_spam_classifier():
    """
    Builds and returns a simple pipeline for spam classification using
    CountVectorizer and Multinomial Naive Bayes.
    """
    # 1. Training examples
    spam_examples = [
        "Congratulations! You’ve won a $1000 gift card. Click here to claim it.",
        "Urgent: Update your bank details immediately to avoid penalty.",
        "Special deal just for you: Buy 1 get 2 free, act now!"
    ]

    not_spam_examples = [
        "Hey Alex, can you review the slides before our meeting tomorrow?",
        "Mom, I’m running late but will be home soon.",
        "Hi Dr. Lee, could you clarify the homework assignment?"
    ]

    # 2. Labels: 1 = Spam, 0 = Not Spam
    X = spam_examples + not_spam_examples
    y = [1, 1, 1, 0, 0, 0]

    # 3. Create a pipeline
    #    - CountVectorizer turns text into numeric features
    #    - MultinomialNB performs Naive Bayes classification
    pipeline = Pipeline([
        ("vectorizer", CountVectorizer()),
        ("classifier", MultinomialNB())
    ])

    # 4. Train the pipeline on our small dataset
    pipeline.fit(X, y)

    return pipeline

def classify_message(message, pipeline):
    """
    Classifies a single message as 'Spam' or 'Not Spam' using the trained pipeline.
    """
    prediction = pipeline.predict([message])[0]
    return "Spam" if prediction == 1 else "Not Spam"

if __name__ == "__main__":
    # Build the model
    model_pipeline = build_spam_classifier()

    # Test it with a new message
    new_message = "Act now to secure your lifetime membership at 70% off—limited offer!"
    result = classify_message(new_message, model_pipeline)
    print(f'Message: "{new_message}"\nClassified as: {result}')
