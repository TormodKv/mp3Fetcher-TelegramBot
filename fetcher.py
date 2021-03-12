import requests
import re
import keys
import json

searchLink = 'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=xxxx&key={0}'.format(keys.youtubeKEY)
youtubeDownloadRoot = 'https://www.yt-download.org/api/button/mp3/'

def fetch(searchWord):

    videoId = ""
    youtubeSearch = searchLink.replace('xxxx', searchWord)

    try:
        rawText = requests.get(youtubeSearch).text
        rawJson = json.loads(rawText)
        videoId = rawJson['items'][0]['id']['videoId']
        title = rawJson['items'][0]['snippet']['title']
        artist = rawJson['items'][0]['snippet']['channelTitle']

        if videoId != "":
            return [videoId, title, artist]
        return ""

    except:
        return ""


def download(videoId, quality, onlyLink = False):
    try:
        html = requests.get(youtubeDownloadRoot + str(videoId)).text
        linkList = re.findall('(?<=href=")(.*)(?=" class)', html)
        for link in linkList:
            if str(link).__contains__('mp3/{}'.format(quality)):
                if onlyLink:
                    return str(link)
                else:
                    mp3 = requests.get(link).content
                    return mp3
        return ""
    except:
        return ""
