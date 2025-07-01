from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from collections import Counter
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv(override=True)

llm = ChatGroq(
    api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
    model="llama-3.1-8b-instant",
    temperature=0.4
)

insight_prompt = PromptTemplate.from_template("""
You are a product review analyst. Based on the following customer reviews, identify:
1. Things that customers generally like and should be maintained (label as "Maintain")
2. Things that customers frequently complain about or need improvement (label as "Improve")
3. Top 3 most crucial improvements needed (label as "Top Improvements")

Only output the result in this format:
**Maintain**
- ...
**Improve**
- ...
**Top Improvements**
- ...
\n\nReviews:\n\n{joined_reviews}
""")

from collections import Counter

def generate_insights(results):
    # Join all reviews for prompt input
    joined_reviews = "\n\n".join(
        f"Title: {r['review_title']}\nDescription: {r['review_description']}\nLLM: {r['sentiment']}"
        for r in results
    )

    response = llm.invoke(insight_prompt.format(joined_reviews=joined_reviews))
    
    if isinstance(response.content, list):
        content = "\n".join(str(item) for item in response.content).strip()
    else:
        content = str(response.content).strip()

    # Parse LLM response
    pros, cons, top_improvements = [], [], []
    current_section = None
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("**Maintain**"):
            current_section = "pros"
        elif line.startswith("**Improve**"):
            current_section = "cons"
        elif line.startswith("**Top Improvements**"):
            current_section = "top"
        elif line.startswith("- "):
            item = line[2:].strip()
            if current_section == "pros":
                pros.append(item)
            elif current_section == "cons":
                cons.append(item)
            elif current_section == "top":
                top_improvements.append(item)

    # Count sentiments
    sentiment_counts = Counter(r["sentiment_class"].lower() for r in results)

    # Generate overall summary
    def generate_overall_summary(analytics):
        pos = analytics.get("positive", 0)
        neg = analytics.get("negative", 0)
        neu = analytics.get("neutral", 0)
        total = pos + neg + neu

        if total == 0:
            return "No reviews available to generate an overall summary."

        pos_ratio = pos / total
        neg_ratio = neg / total

        if pos_ratio > 0.6:
            return "🟢 The product is highly appreciated by users and is **strongly recommended** for purchase."
        elif pos_ratio > 0.4 and neg_ratio < 0.3:
            return "🟡 The product receives mixed but generally favorable reviews. It is **acceptable** for most buyers."
        else:
            return "🔴 The product has received predominantly negative feedback and is **not recommended** at this time."

    summary = generate_overall_summary(sentiment_counts)

    return {
        "pros": pros,
        "cons": cons,
        "top_improvements": top_improvements,
        "analytics": dict(sentiment_counts),
        "summary": summary  
    }