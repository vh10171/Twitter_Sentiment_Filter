import streamlit as st
import pandas as pd
from textblob import TextBlob
import tweepy
import plotly.express as px
import matplotlib.pyplot as plt
import time
time.sleep(5)  # sleep 5 seconds between calls
# Twitter API setup
BEARER_TOKEN = "YOUR_BEARER_TOKEN"
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

st.title("Twitter Sentiment Filter")
query = st.text_input("Search Tweets About:")
if query:
    response = client.search_recent_tweets(query=query, max_results=10)
    
    if response.data:
        tweets = []
        for tweet in response.data:
            polarity = TextBlob(tweet.text).sentiment.polarity
            label = "Negative" if polarity < -0.1 else "Positive/Neutral"
            tweets.append({"Tweet": tweet.text, "Sentiment": label, "Score": polarity})

        df = pd.DataFrame(tweets)
        st.dataframe(df)

        # Sentiment count chart
        st.subheader("Sentiment Distribution")
        sentiment_counts = df["Sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]

        fig = px.bar(sentiment_counts, x="Sentiment", y="Count", color="Sentiment",
                     color_discrete_map={"Positive/Neutral": "green", "Negative": "red"})
        st.plotly_chart(fig)

        # Sentiment score histogram
        st.subheader("Sentiment Score Distribution")
        fig2, ax = plt.subplots()
        df["Score"].hist(bins=10, ax=ax, color='skyblue', edgecolor='black')
        ax.set_title("Polarity Score Histogram")
        ax.set_xlabel("Sentiment Polarity")
        ax.set_ylabel("Tweet Count")
        st.pyplot(fig2)

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "tweets.csv", "text/csv")
    else:
        st.warning("No tweets found for this query.")
