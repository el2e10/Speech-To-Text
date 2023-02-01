import numpy as np
import pandas as pd
import streamlit as st
from dashboard_data_helper import *

manifest_df = pd.read_json("train_manifest.jsonl", lines=True)
unique_alphabets = get_alphabet_size(manifest_df)

st.title("Speech Data Explorer")

st.header("Data Statistics")

one, three, four = st.columns(3)
one.metric(label="Total Number of Hours", value=get_total_hours(manifest_df))
# two.metric(label="Total Number of Utterances", value="None")
three.metric(label="Vocabulary Size", value=get_vocab_size(manifest_df))
four.metric(label="Alphabet Size", value=len(unique_alphabets))


st.header("Visual Statistics")

st.subheader('Alphabets in the dataset')
st.code(unique_alphabets)

st.subheader("Duration per file")
st.bar_chart(get_duration_per_file(manifest_df))

st.subheader("Number of words per file")
st.bar_chart(get_num_of_word(manifest_df))

st.subheader("Number of characters per file")
st.bar_chart(get_num_of_characters(manifest_df))
