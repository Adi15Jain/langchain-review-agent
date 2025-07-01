import streamlit as st
import json
import os
from doc import content

# Load the results file
with open("results.json", "r") as f:
    result_data = json.load(f)
    results = result_data.get("reviews", [])
    product_title = result_data.get("product_title", "Amazon Product")

# Load insights if available
final_insights = {}
if os.path.exists("insights.json"):
    with open("insights.json") as f:
        final_insights = json.load(f)

st.set_page_config(page_title="Review Sentiment Viewer", layout="centered")
st.title(f"📝 Review Sentiment Analyzer: {product_title}")

with st.expander("📊 Sentiment Analytics"):
    # Display analytics if available
    if "analytics" in final_insights:
        for sentiment, count in final_insights["analytics"].items():
            st.markdown(f"- **{sentiment.capitalize()}**: {count} reviews")
    if "summary" in final_insights:
        st.markdown("### 🧾 Overall Product Summary")
        summary = final_insights["summary"]
        if "strongly recommended" in summary:
            st.success(summary)
        elif "acceptable" in summary:
            st.warning(summary)
        elif "not recommended" in summary:
            st.error(summary)
        else:
            st.info(summary)


if final_insights:
    with st.expander("🔍 Product Insights"):
        if final_insights.get("pros"):
            st.markdown("### ✅ What to Maintain")
            for pro in final_insights["pros"]:
                st.markdown(f"- {pro}")

        if final_insights.get("cons"):
            st.markdown("### ❌ What Needs Improvement")
            for con in final_insights["cons"]:
                st.markdown(f"- {con}")

        if final_insights.get("top_improvements"):
            st.markdown("### 📌 Suggested Top Improvements")
            for tip in final_insights["top_improvements"]:
                st.markdown(f"- **{tip}**")


# Display reviews
with st.expander("🧠 Product Reviews and Reasonings:"):
    for i, entry in enumerate(results, 1):
        st.markdown(f"### Review #{i}")
        
        st.markdown(f"**Title:** {entry.get('review_title', 'N/A')}")
        st.markdown(f"**Description:** {entry.get('review_description', 'N/A')}")
        st.markdown(f"**Rating:** ⭐ {entry.get('rating', 'N/A')}")
        
        sentiment = entry.get("sentiment_class", "Unknown").lower()
        if sentiment == "positive":
            badge_text, badge_color = "🟢 Positive", "green"
        elif sentiment == "negative":
            badge_text, badge_color = "🔴 Negative", "red"
        elif sentiment == "neutral":
            badge_text, badge_color = "🟡 Neutral", "orange"
        else:
            badge_text, badge_color = "⚪ Unknown", "gray"

        st.markdown(f"**Sentiment:** :{badge_color}[{badge_text}]")

        reasoning = entry.get("sentiment", "")
        with st.expander("🤖 Sentiment Reasoning"):
            st.write(reasoning)

        st.markdown("---")


with st.expander("📄 Project Documentation", expanded=False):
    st.markdown(content)