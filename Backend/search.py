import requests
from typing import List
from termcolor import colored
from abc import ABC, abstractmethod

class VideoProvider(ABC):
    @abstractmethod
    def search(self, query: str, api_key: str, it: int, min_dur: int) -> List[str]:
        pass

class PexelsProvider(VideoProvider):
    def search(self, query: str, api_key: str, it: int, min_dur: int) -> List[str]:
        headers = {"Authorization": api_key}
        qurl = f"https://api.pexels.com/videos/search?query={query}&per_page={it}"
        r = requests.get(qurl, headers=headers)
        response = r.json()
        video_urls = []
        try:
            for i in range(it):
                if response["videos"][i]["duration"] < min_dur:
                    continue
                raw_urls = response["videos"][i]["video_files"]
                temp_video_url = ""
                video_res = 0
                for video in raw_urls:
                    if ".com/video-files" in video["link"]:
                        if (video["width"] * video["height"]) > video_res:
                            temp_video_url = video["link"]
                            video_res = video["width"] * video["height"]
                if temp_video_url:
                    video_urls.append(temp_video_url)
        except Exception as e:
            print(colored(f"[-] Pexels: No videos found for '{query}'.", "red"))
            print(colored(e, "red"))
        print(colored(f"\t=> Pexels: Found {len(video_urls)} videos for '{query}'", "cyan"))
        return video_urls

class PixabayProvider(VideoProvider):
    def search(self, query: str, api_key: str, it: int, min_dur: int) -> List[str]:
        qurl = f"https://pixabay.com/api/videos/?key={api_key}&q={query}&per_page={it}"
        r = requests.get(qurl)
        response = r.json()
        video_urls = []
        try:
            for video in response["hits"]:
                if video.get("duration", 0) < min_dur:
                    continue
                # Pixabay provides videos in different qualities, choose the largest one
                if "large" in video["videos"]:
                    video_urls.append(video["videos"]["large"]["url"])
                elif "medium" in video["videos"]:
                    video_urls.append(video["videos"]["medium"]["url"])
                elif "small" in video["videos"]:
                    video_urls.append(video["videos"]["small"]["url"])
        except Exception as e:
            print(colored(f"[-] Pixabay: No videos found for '{query}'.", "red"))
            print(colored(e, "red"))
        print(colored(f"\t=> Pixabay: Found {len(video_urls)} videos for '{query}'", "cyan"))
        return video_urls

def search_for_stock_videos(query: str, pexels_api_key: str, pixabay_api_key: str, it: int, min_dur: int) -> List[str]:
    providers = []
    if pexels_api_key:
        providers.append(PexelsProvider())
    if pixabay_api_key:
        # pyrefly: ignore  # bad-argument-type
        providers.append(PixabayProvider())

    all_video_urls = []
    for provider in providers:
        api_key = pexels_api_key if isinstance(provider, PexelsProvider) else pixabay_api_key
        video_urls = provider.search(query, api_key, it, min_dur)
        all_video_urls.extend(video_urls)

    return all_video_urls
