# Data Engineering(Speech To Text)

## Setup
```
pip install -r requirements.txt
```
Additional tools required
- [GNU Parallel](https://www.gnu.org/software/parallel/)
- [FFmpeg](https://ffmpeg.org/) 

## Introduction
The project aims to create a data engineering pipeline for curating a Speech-To-Text dataset. The data is collected from publicly available lectures on NPTEL. The audio and corresponding transcription are collected from the website for creating the dataset.

## Stages of pipeline 
- Downloading Audio and Transcript
    - NPTEL has all their lectures uploaded to youtube. The audio from these videos can be directly extracted using a tool called 'yt-dlp'. 
    - The transcripts from the videos are saved in pdf files and stored in google drive. To download the pdf from google drive a python package called 'gdown' is used.
    - All the links to the resources can be scraped from their course page.
    <!-- - To extract the audio and txt data run the following command -->
    ```python
    from data_collector import DataCollector

    collector = DataCollector(course_id)
    collector.execute()

    # The audio will be stored in Data/Audio and transcript in Data/Transcripts
    ```
- Preprocessing audio
    - The data downloaded from youtube will be in .webm format we convert it into .wav format with a 16KHz sampling rate and mono channel format.
    - A shell script called 'audio_preprocessor.sh' is used for conversion.
    - To make the conversion faster by parallelizing code across n CPUs a tool called 'GNU parallel' is used.
    - For every audio there is a 10-second intro and 32-second end credits this portion of the data is audio is removed as they don't have any speech. 
    - To perform audio preprocessing run the following bash command.
    ```bash
    bash audio_preprocessor.sh audio_directory_path output_directory_path
    ```
- Preprocessing text
    - The transcript files in the pdf is converted into txt files in this state of the pipeline.
    - The text undergoes some preprocessing like removal of punctuations and converting to lowercase.
    - The numerical data in the text is converted to words(eg. 10 -> ten).
    <!-- - To perform text preprocessing run the following command. -->
    ```python
    from text_preprocessor import TextPreprocessor

    preprocessor = TextPreprocessor(transcript_directory)
    preprocessor.execute()
    ```
- Create a training manifest file
    - The output of the data pipeline is a JSON lines file that contains details like audio_filepath, duration, and text. 
    <!-- - To create training manifest file run the following command -->
    ```python
    from manifest_generator import ManifestGenerator

    generator = ManifestGenerator(preprocessed_audio_directory, preprocessed_transcript_directory)
    gnerator.execute()
    ```

- Create a dashboard
    - Dashboard shows some visualization and metrics of text, and audio contents.
    - To see the dashboard run the following command.
    ```
    streamlit dashboard.py
    ```

### Note
Please refer 'testing.py' file for understanding how to run the programs.