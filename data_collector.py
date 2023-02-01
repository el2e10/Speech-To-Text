import requests
from pathlib import Path

import yt_dlp
import gdown

class DataCollector():
    def __init__(self, course_id):
        self.TRANSCRIPT_DOWNLOAD_URL = f"https://tools.nptel.ac.in/npteldata/downloads.php?id={course_id}"
        self.VIDEO_DOWNLOAD_URL = f"https://tools.nptel.ac.in/npteldata/course_outline1.php?id={course_id}"
        self.audio_path, self.transcript_path = self._create_data_directories()

    def _create_data_directories(self):
        audio_path = Path("Data/Audio")
        transcript_path = Path("Data/Transcripts")
        audio_path.mkdir(parents=True, exist_ok=True)
        transcript_path.mkdir(parents=True, exist_ok=True)
        return audio_path, transcript_path 


    def _get_page_data(self):
        headers = {
            'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
        }
        transcript_download_page = requests.get(self.TRANSCRIPT_DOWNLOAD_URL, headers=headers)
        video_download_page = requests.get(self.VIDEO_DOWNLOAD_URL, headers=headers)
        video_result_dict, transcript_result_dict = dict(video_download_page.json()), dict(transcript_download_page.json())
        return video_result_dict, transcript_result_dict
    
    def _extract_video_urls(self, video_result_dict):
        video_units_data = video_result_dict['data']['units']
        video_download_urls = [{'url': "https://www.youtube.com/watch?v="+lesson['youtube_id'], 'lesson_id': f"{lesson['name']}_{str(lesson['id'])}"} for unit in video_units_data for lesson in unit['lessons']]
        return video_download_urls

    def _extract_transcript_urls(self, transcript_result_dict):
        transcript_download_urls =[{'url': y['url'], 'lesson_id': f"{x['title']}_{str(x['lesson_id'])}"} for x in transcript_result_dict['data']['transcripts'] for y in x['downloads'] if y['language'] == 'english-Verified'] 
        transcript_download_urls = [{'url': f"https://drive.google.com/uc?id={x['url'].split('/')[-2]}", 'lesson_id': x['lesson_id']} for x in transcript_download_urls]
        return transcript_download_urls

    def _download_audio_files(self, audio_urls):
        download_audio_filepath = []

        def _yt_dlp_monitor(video_download_info):
            status = video_download_info.get('status', 'downloading')
            if(status == 'finished'):
                audio_file_path = video_download_info.get("info_dict").get("_filename")
                download_audio_filepath.append(audio_file_path)

        # audio_urls = audio_urls[:3]
        audio_urls = audio_urls
        ydl_opts = {'format': 'bestaudio', 
            'progress_hooks': [_yt_dlp_monitor],
            'quiet': True,
            'paths': {'home': str(self.audio_path)}}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([x['url'] for x in audio_urls])

        new_names = [x['lesson_id'] for x in audio_urls]
        self._rename_audio_files(download_audio_filepath, new_names)
    
    def _rename_audio_files(self, current_names, new_names):
        for current_name, new_name in zip(current_names, new_names):
            path = Path(current_name)
            path.replace(path.with_name(f"{new_name}{path.suffix}"))

    def _download_transcript_file(self, transcript_urls):
        # for url in transcript_urls[:3]:
        for url in transcript_urls:
            gdown.download(url['url'], f"{self.transcript_path}/{url['lesson_id']}.pdf", quiet=True)

    def execute(self):
        video_dict, transcript_dict = self._get_page_data()
        audio_urls = self._extract_video_urls(video_dict)
        transcript_urls = self._extract_transcript_urls(transcript_dict)
        self._download_audio_files(audio_urls)
        self._download_transcript_file(transcript_urls)
        return self.audio_path, self.transcript_path

if __name__ == '__main__':
    data_collector = DataCollector(106106184)
    data_collector.execute()
    # video_dict, transcript_dict = data_collector._get_page_data()
    # audio_urls = data_collector._extract_video_urls(video_dict)
    # data_collector._download_audio_files(audio_urls)