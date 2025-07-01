import os
import dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from pydantic import SecretStr

dotenv.load_dotenv()

llm = ChatGroq(
    api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
    model="qwen-qwq-32b",
    temperature=0.3
)

template = PromptTemplate.from_template(
    "Classify the sentiment of the following e-commerce review as Positive, Negative, or Neutral.\n\nReview: \"{review}\""
)

def classify_review(review: str) -> dict:
    prompt = template.format(review=review)
    response = llm.invoke(prompt)

    output = str(response.content if hasattr(response, "content") else response).strip()

    sentiment_class = "Unknown"

    for sentiment in ["Positive", "Negative", "Neutral"]:
        if sentiment.lower() in output.lower():
            sentiment_class = sentiment.capitalize()
            break

    return {
        "sentiment": output,            
        "sentiment_class": sentiment_class  
    }
