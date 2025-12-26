from pytubefix import YouTube
from pytubefix import Playlist
try:
    choice=int(input("1.Playlist\n2.Video\nEnter a choice you want to download: "))
except:
    
    print("Enter a number")

    choice=int(input("1.Playlist\n2.Video\nEnter a choice you want to download: "))
if choice==1:
    ch="Playlist"
else:
    ch="Video"
URL = input(f"Enter the Url of {ch} you want to download: ")


if choice!=1:
    while True:
        if "https" in URL:
            try:
                yt = YouTube(URL)

                stream = yt.streams.get_highest_resolution()
                stream.download("download")

                print("Download complete!")
            except:
                print("please enter a valid url the url you entered is not working.")
            break
        else:
            newURL=f"https://{URL}"
            URL=newURL
else:
    try:
        pl = Playlist(URL)
        print(f"Found {len(pl.video_urls)} videos in the playlist.")
        for url in pl.video_urls:
            try:
                video = YouTube(url)
                stream = video.streams.get_highest_resolution()
                stream.download("download/playlist")
                print(f"Downloaded: {video.title}")
            except:
                print(f"Failed to download video: {url}")
        print("All playlist videos downloaded!")
    except:
        print("Invalid playlist URL. Please check the link.")