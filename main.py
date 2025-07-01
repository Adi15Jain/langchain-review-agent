import os
import json
import time
import random
from agent.review_scraper import fetch_reviews_from_apify
from agent.classifier import classify_review
from agent.generate_insights import generate_insights
from dotenv import load_dotenv

load_dotenv(override=True)

def safe_classify(review_text, retries=5):
    for attempt in range(retries):
        try:
            return classify_review(review_text)
        except Exception as e:
            wait = (2 ** attempt) + random.random()
            print(f"⚠️ Error: {e} (retrying in {wait:.2f}s)")
            time.sleep(wait)
    raise RuntimeError("❌ Failed to classify review after multiple retries")

def main():
    dataset_id = os.getenv("APIFY_DATASET_ID")
    if not dataset_id:
        raise ValueError("APIFY_DATASET_ID is not set in the .env file")

    reviews = fetch_reviews_from_apify(dataset_id)
    results = []
    sentiment_counter = {"positive": 0, "negative": 0, "neutral": 0}
    all_descriptions = []

    for i, review_dict in enumerate(reviews, 1):
        full_review_text = f"Title: {review_dict.get('reviewTitle', '')}\nDescription: {review_dict.get('reviewDescription', '')}"
        response = classify_review(full_review_text)

        sentiment_class = response["sentiment_class"].lower()
        sentiment_counter[sentiment_class] += 1

        results.append({
            "review_title": review_dict.get("reviewTitle", ""),
            "review_description": review_dict.get("reviewDescription", ""),
            "rating": review_dict.get("ratingScore", ""),
            "sentiment_class": sentiment_class,
            "sentiment": response["sentiment"],
        })

        all_descriptions.append(full_review_text)

    # Save review-level results (simple format)
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

    # Generate insights
    insights = generate_insights(results)

    final_insights = {
        "pros": insights.get("pros", []),
        "cons": insights.get("cons", []),
        "top_improvements": insights.get("top_improvements", []),
        "analytics": sentiment_counter,
        "summary": insights.get("summary", ""),
        "recommendation": insights.get("recommendation", ""),
    }

    with open("insights.json", "w") as f:
        json.dump(final_insights, f, indent=4)

    print("✅ Done.")

if __name__ == "__main__":
    main()
