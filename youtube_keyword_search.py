import streamlit as st
import pandas as pd
from youtubesearchpython import VideosSearch


def search_video(kw, limit=20, region="BR", df=True):
    videosSearch = VideosSearch(kw, limit = limit, region=region)
    if df:
        data = pd.json_normalize(videosSearch.result()["result"])
        data['viewCount'] = data['viewCount.text'].str.replace(" views", "")
        data['viewCount'] = data['viewCount'].str.replace(",", "").astype(int)
        cols = [
            'title',
            'viewCount',
            'channel.name',
            'duration' ,
            'link',
            ]
        return data.loc[:, cols].sort_values("viewCount", ascending=False)
    else:
        return videosSearch.result()["result"]

st.title('Youtube keyword search')

keywords = st.text_input('Youtube keywords', 'como trabalhar nos estados unidos')

data_load_state = st.text('Searching...')
data = search_video(keywords)
data
data_load_state.text("Done!")

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')


csv = convert_df(data)

st.download_button(
   "Download your search data",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
