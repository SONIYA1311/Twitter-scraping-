# importing all the required libraries
import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import json
st.title("TWITTER SCRAPING")
client = pymongo.MongoClient("mongodb://localhost:27017")
database = client.Twitter_scraping
collection = database.Scraped_data
keyword = st.text_input("ENTER THE KEYWORD OR HASHTAG")
max_count = st.number_input("MAXIMUM TWEET COUNT")
from_date = st.date_input("FROM DATE")
to_date = st.date_input("TO DATE")
if st.checkbox("DISPLAY SCRAPED DATA"):
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{from_date} until:{to_date}").get_items()):
        if i > max_count:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount,
                            tweet.retweetCount, tweet.lang, tweet.sourceLabel, tweet.likeCount])

    tweets_df = pd.DataFrame(tweets_list, columns=["DateTime", "TweetID", "URL", "Tweet Content", "UserName", "ReplyCount",
                                                   "ReTweet Count", "Language", "Source", "Like Count"])
    st.dataframe(tweets_df)
    x = tweets_df.to_dict('records')
    def convert_df(tweets_df):
        return tweets_df.to_csv()
    csv = 'convert_df(tweets_df)'
    if st.download_button(label="DOWNLOAD CSV", data=csv, file_name="scraped_data.csv", mime="text/csv"):
         st.write("DOWNLOADED CSV FILE SUCCESSFULLY")
    def convert_df(tweets_df):
        return tweets_df.to_json()
    json = 'convert_df(tweets_df)'
    if st.download_button(label="DOWNLOAD JSON", data=json, file_name="scraped_data.json", mime="text/json"):
        st.write("DOWNLOADED JSON FILE SUCCESSFULLY")
    if st.button("UPLOAD DATA INTO MONGODB"):
        collection.insert_many(x)
        for each in collection.find():
            print(each)
        st.write("UPLOADED DATA SUCCESSFULLY")

