import scrapetube
import random
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

file_path = 'index.html'

channelList = ['fireship', 'codyko', 'jomboymedia', 'hannahmeloche', 'codyko2', 'danny', 'dannymullenofficial', 'VASAviation', 'squatuniversity', 'westcoastflyer', 'CitationMax',
'sickos', 'kboges', 'mrbeast', 'prestongoes', 'BodyweightWarrior', 'CodeBlueCam', 'clixlive', 'AirSafetyInstitute']
videoFeed = [] #title, username, date, videoID, thumbnailLink, views]

insertIntoHTML = ''

def getRecentVidLinksFromChannel(yt_username):
    videoList = scrapetube.get_channel(channel_username=yt_username, limit=3, sort_by="newest" )

    # grabs the youtube video URL from data, and adds to list
    for video in videoList:
        videoData = []

        #extracts all data from the dictionary and creates a video object and adds to array
        videoData.append(video['title']['runs'][0]['text'])
        videoData.append(video['title']['accessibility']['accessibilityData']['label'].split('by ')[-1].split(' ')[0])
        videoData.append(video['publishedTimeText']['simpleText'])
        videoData.append(video['videoId'])
        videoData.append(video['thumbnail']['thumbnails'][3]['url'])
        videoData.append(video['viewCountText']['simpleText'])

        videoFeed.append(videoData)


# loops each channel in channel list, takes 3 most recent videos, and adds object to videoFeed
def getVidsFromEveryChannel():
    for channel in channelList:
        getRecentVidLinksFromChannel(channel)

getVidsFromEveryChannel()

# turn date string into a datetime object
def parse_date(date_str):
    if 'day' in date_str:
        days_ago = int(date_str.split()[0])
        return datetime.now() - timedelta(days=days_ago)
    elif 'week' in date_str:
        weeks_ago = int(date_str.split()[0])
        return datetime.now() - timedelta(weeks=weeks_ago)
    elif 'month' in date_str:
        months_ago = int(date_str.split()[0])
        return datetime.now() - timedelta(days=30 * months_ago)  # Approximation
    elif 'hour' in date_str:
        hours_ago = int(date_str.split()[0])
        return datetime.now() - timedelta(hours=hours_ago)
    else:
        return datetime.min  # If date is not recognized

# sort by date
def sort_videos_by_date(videos):
    """Sort the list of videos by date."""
    return sorted(videos, key=lambda video: parse_date(video[2]), reverse=True)

videoFeed = sort_videos_by_date(videoFeed)

# creates html attribute for each video in videoFeed []
def createVideo(title, username, date, videoID, thumbnailLink, views):
    return f'''
<div class="thumbnail">
    <a href="https://xoutu.be/{videoID}">
        <img src="{thumbnailLink}">
    </a>
     <h2 class="title">{title}</h2>
    <h3 class="subtitle">{username} - {date} - {views}</h3>
    <div class="horizontal-line"></div>
</div>
'''


# prints all the videos in videoFeed in HTML format
for item in videoFeed:
    insertIntoHTML += createVideo(item[0], item[1], item[2], item[3], item[4], item[5])


# write to index.html
with open(file_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'lxml')

target_div = soup.find('div', id='target-div')

if target_div:
    target_div.clear()
    target_div.append(BeautifulSoup(insertIntoHTML, 'html.parser'))

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

print(f"Successfully updated {file_path}")