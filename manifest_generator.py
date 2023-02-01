import json
from pathlib import Path

import librosa

class ManifestGenerator():
    def __init__(self, audio_directory, transcript_directory):
        self.audio_directory = Path(audio_directory)
        self.transcript_directory = Path(transcript_directory)

    def _get_audio_duration(slef, audio_file):
        return librosa.get_duration(filename=audio_file)

    def _get_txt_data(self, txt_file):
        txt_data = ""
        with open(txt_file, "r") as txt_fp:
            txt_data = txt_fp.read()
        return txt_data

    def execute(self):
        with open("train_manifest.jsonl", "a+") as jsonl_fp:
            for file in self.audio_directory.iterdir():
                txt_file_path = self.transcript_directory / f"{file.stem}.txt"
                if (not txt_file_path.exists()):
                    continue
                audio_file = str(file)
                audio_duration = self._get_audio_duration(audio_file)
                transcript_data = self._get_txt_data(txt_file_path)

                json_record = json.dumps({'audio_filepath': audio_file, 'duration': audio_duration, 'text': transcript_data})
                jsonl_fp.write(json_record + "\n")
            
            return jsonl_fp
  
if __name__ == '__main__':
    manifest_generator = ManifestGenerator('Data/Preprocessed', 'Data/Transcripts')
    manifest_generator.execute()