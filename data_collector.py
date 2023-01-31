import requests
from pathlib import Path

import yt_dlp
import gdown

class DataCollector():
    def __init__(self, course_id):
        self.TRANSCRIPT_DOWNLOAD_URL = f"https://tools.nptel.ac.in/npteldata/downloads.php?id={course_id}"
        self.VIDEO_DOWNLOAD_URL = f"https://tools.nptel.ac.in/npteldata/course_outline1.php?id={course_id}"

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
        video_download_urls = ["https://www.youtube.com/watch?v="+lesson['youtube_id'] for unit in video_units_data for lesson in unit['lessons']]
        return video_download_urls

    def _extract_transcript_urls(self, transcript_result_dict):
        transcript_download_urls =[y['url'] for x in transcript_result_dict['data']['transcripts'] for y in x['downloads'] if y['language'] == 'english-Verified'] 
        transcript_download_urls = [f"https://drive.google.com/uc?id={x.split('/')[-2]}" for x in transcript_download_urls]
        return transcript_download_urls

    def _download_audio_files(self, audio_urls):
        audio_urls = audio_urls[:10]
        ydl_opts = {'format': 'bestaudio'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in audio_urls:
                error_code = ydl.download(url)

    def _download_transcript_file(self, transcript_urls):
        for url in transcript_urls[:10]:
            gdown.download(url, "t.pdf", quiet=True)


if __name__ == '__main__':
    data_collector = DataCollector(106106184)
    video_dict, transcript_dict = data_collector._get_page_data()
    print(data_collector._extract_transcript_urls(transcript_dict))