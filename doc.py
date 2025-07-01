content = """
## 🧠 Project Overview — Amazon Review Sentiment Analyzer

This tool uses **LangChain** and **LLaMA 4 (via Groq)** to classify Amazon product reviews as **Positive**, **Negative**, or **Neutral**, then applies a RAG-based method to generate product improvement insights and an overall recommendation summary. The results are displayed in an interactive **Streamlit** web interface.

---

### 🔧 Technologies Used

- **LangChain + Groq (LLaMA 4)** — For LLM-based sentiment classification and RAG-based product insights.
- **Apify** — For Amazon product review scraping via API.
- **Streamlit** — Interactive and expandable frontend UI.
- **Python + dotenv** — Modular backend and configuration management.

---

### 🔄 Workflow

1. **.env Configuration:**
   - Stores keys like `GROQ_API_KEY`, `APIFY_API_KEY`, and `APIFY_DATASET_ID`.
   - Automatically loads credentials and dataset for scraping and classification.

2. **Review Scraping (`review_scraper.py`):**
   - Uses the Apify API to scrape a large number of Amazon product reviews (supports up to 50,000).
   - Extracts fields such as `reviewTitle`, `reviewDescription`, and `ratingScore`.

3. **Classification (`classifier.py`):**
   - Combines title and description per review.
   - Uses a LangChain `PromptTemplate` to instruct the LLM to classify sentiment.
   - Parses the LLM response to extract:
     - `sentiment`: Explanation text.
     - `sentiment_class`: One of [Positive, Negative, Neutral].

4. **Insight Generation (`generate_insights.py`):**
   - Applies a RAG-based (Retrieval-Augmented Generation) approach.
   - Aggregates LLM responses to extract:
     - ✅ Pros (what to maintain)
     - ❌ Cons (what to improve)
     - 📌 Top Improvements (actionable suggestions)
   - Also calculates overall sentiment distribution.
   - Uses rule-based logic to generate an overall product summary and recommendation.

5. **Backend Script (`main.py`):**
   - Orchestrates review classification and insight generation.
   - Saves outputs into `results.json` (individual review classifications) and `insights.json` (overall insights).

6. **Frontend UI (`app.py`):**
   - Loads and displays:
     - 🔍 Each review's title, description, rating, sentiment badge, and reasoning
     - 📊 Sentiment distribution stats
     - ✅/❌ Product pros and cons
     - 📌 Suggested improvements
     - 🧾 Final summary & purchase recommendation

---

### 🌱 Future Enhancements

- 📈 Graphical visualization for sentiment trends
- 🎯 Sentiment-based review filtering
- 🛒 Multi-product comparison interface
- 🗃️ Persistent database integration for long-term storage
- 🧠 LLM-generated star ratings and summaries per review
"""
