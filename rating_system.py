from transformers import pipeline

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def predict_real_or_fake(review_text):
    result = classifier(review_text)

    label = result[0]['label']
    confidence = result[0]['score']
    
    if label == "FAKE":
        credibility_score = 100 - confidence  # 假評論分數較低
    else:
        credibility_score = confidence  # 真實評論分數較高
    
    return round(credibility_score, 2)

# 測試
if __name__ =="__main__":
    sample_review = "This product is amazing! It works perfectly and exceeded my expectations."
    score = predict_real_or_fake(sample_review)
    print(f"Predicted credibility score for the review: {score}")
