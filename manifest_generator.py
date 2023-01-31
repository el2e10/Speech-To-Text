import json
from pathlib import Path

import librosa

class ManifesGenerator():
    def __init__(self, audio_directory, transcript_directory):
        self.audio_directory = Path(audio_directory)
        self.transcript_directory = Path(transcript_directory)

    def _get_audio_duration(slef, audio_file):
        return librosa.get_duration(filename=audio_file)

    def _get_txt_data(self, txt_file):
        txt_data = ""
        with open(txt_file, "r") as txt_fp:
            txt_data = txt_file.read()
        return txt_data

    def execute(self):
        for file in self.audio_directory.iterdir():
            audio_file = str(file)
            transcript_file = transcript_directory / f"{file.stem}.txt"
            audio_duration = get_audio_duration(audio_file)
            transcript_data = get_txt_data(transcript_file)

            json_record = json.dumps({'audio_filepath': audio_file, 'duration': audio_duration, 'text': transcript_data})
            jsonl_fp.write(json_record + "\n")
  
