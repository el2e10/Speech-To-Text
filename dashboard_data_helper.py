import librosa
import pandas as pd
from pathlib import Path


def get_total_hours(manifest_df):
    return manifest_df.duration.sum()

def get_vocab_size(manifest_df):
    unique = manifest_df.text.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis=0)
    return len(unique)

def get_alphabet_size(manifest_df):
    vocab = manifest_df.text.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis=0)
    unique = vocab.index.to_series().apply(lambda x: pd.value_counts(list(x))).sum(axis=0)
    # print(unique)
    return unique.index.values

def get_duration_per_file(manifest_df):
    return manifest_df.duration.values

def get_num_of_word(manifest_df):
    return manifest_df.text.apply(lambda x: len(x.split())).values

def get_num_of_characters(manifest_df):
    return manifest_df.text.apply(lambda x: len(x)).values

# print(get_total_hours(Path("Data/Preprocessed")))