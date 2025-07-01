To run this project:

1. Clone the GitHub Repository, move to next step if already done.
2. Open the langchain-review-agent project folder and open a terminal from the root.
3. Create a venv (virtual environment) by executing the following commands:
   -python -m venv .venv
   -source venv/bin/activate
4. Install the requirements (Can be found in "req.txt").
5. Get your own API_KEYS from GROQ and APIFY and place them in the .env (environment variable file).
6. Go to apify store and use the api of your choice.
7. Then log on to apify get dataset_id of your scraped content, this will allow your main app to fetch the content.
8. Once you've added your desired dataset_id, run main.py, once it is executed completely oyu will receive two json files: insights and reviews.
9. Lastly run the streamlit app using the command "streamlit run app.py" to see the results on the web.

Note: These JSON files are just for testing the streamlit app, you can get your own dataset_id and use the json file of your preference.
