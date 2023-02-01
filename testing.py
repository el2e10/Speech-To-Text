import subprocess

from data_collector import DataCollector
from text_preprocessor import TextPreprocessor
from manifest_generator import ManifestGenerator

data_collector = DataCollector(106106184)
audio_path, transcript_path = data_collector.execute()

preprocessed_audio_location = "Data/Preprocessed"

subprocess.run(f"bash audio_preprocessor.sh Data/Audio {preprocessed_audio_location}", shell=True)

text_preprocessor = TextPreprocessor(transcript_path)
text_preprocessor.execute()

manifest_generator = ManifestGenerator(preprocessed_audio_location, "Data/Transcripts")
manifest_generator.execute()