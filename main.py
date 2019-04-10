import requests
from bs4 import BeautifulSoup
import brotli
from urllib.parse import unquote


def probe_sources(url):
    headers = {
        'authority': 'www16.kickassanime.io',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'referer': ''.join(url.split('/')[:-1]),
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cfduid=dec0b52121ccda1df268af3329771adc51547643530; _ga=GA1.2.1276448699.1547643543; BB_plg=pm; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A4%2C%22TejndEEDj%22%3A%22-Vd1qEq5%2B%22%7D%2C%22C171460%22%3A%7B%22page%22%3A2%2C%22time%22%3A1551072219811%7D%2C%22C293329%22%3A%7B%22page%22%3A2%2C%22time%22%3A1551072219936%7D%7D; UUID=e3cbd280-3b7c-11e9-a1ec-f8bc12538e34; bbbi=16a6d6e3-c9b9-43d4-bd84-659a89441a03',
    }

    response = requests.get(url, headers=headers)

    html = brotli.decompress(response.content)

    soup = BeautifulSoup(html, "lxml")

    video_container_div = soup.find("div", attrs={"class":"col-sm-6"})

    anchors = video_container_div.findAll("a")
    iframes = video_container_div.findAll("iframe")

    video_src = []

    for iframe in iframes:
        src = iframe.get("src")
        if src != None:
            src_2 = src.split("data=")[1].split("&vref")[0]
            src_3 = unquote(src_2)
            video_src.append(src_3)

    for anchor in anchors:
        src = anchor.get("data-video")
        if src != None:
            video_src.append(src)
            
    return video_src

def prepare_sources(video_src):
    video_src2 = []

    for src in video_src:
        if "vidstreaming.io" in src:
            src = src.replace("streaming.php","download")
            src = src.replace("load.php", "download")
            src = "https:" + src
        elif "estream.to" in src:
            pass
        elif "animo-pace-stream.io" in src:
            pass
        elif "openload.co" in src:
            pass
        elif "oload.tv" in src:
            pass
        elif "bestream.tv" in src:
            pass
        elif "yourupload.com" in src:
            src = src.replace("embed","watch")
        elif "streamango.com" in src:
            pass
        else:
            print("Unknown:",src)
        video_src2.append(src)

    video_src2 = set(video_src2)

    return video_src2

def final_sources(video_src2):

    download_src = {}
    
    c = 0
    for src in video_src2:
        if "vidstreaming.io" in src:
            response = requests.get(src)
            soup = BeautifulSoup(response.text, "lxml")
            src = soup.find("div", attrs={"class":"dowload"}).find("a").get("href")
            download_src["vidstreaming.io"] = src
        elif "estream.to" in src:
            pass
        elif "animo-pace-stream.io" in src:
            pass
        elif "openload.co" in src:
            pass
        elif "oload.tv" in src:
            pass
        elif "bestream.tv" in src:
            pass
        elif "yourupload.com" in src:
            print(src)
            response = requests.get(src)
            soup = BeautifulSoup(response.text, "lxml")
            src = "https://www.yourupload.com"+soup.find("a", attrs={"class":"btn btn-success"}).get("href")
            anime_id = src.split("=")[1].split("&")[0]
            token = "234c"
            headers = {
                'authority': 'www.yourupload.com',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'referer': src,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': '__cfduid=dacc5fbf2a62bbf413300e0b709e2483a1550203790; connect.sid=s%3AlTXyiW8C2ElNUqJWY6DokH-b6QwFRvbk.lWjrlpM6GWnTOrV0BNIU%2Bk5f83Jf8BgPSXBR2FiAcDU; _ga=GA1.2.22425615.1554793618; _gid=GA1.2.577874818.1554901786; _gat_gtag_UA_51999698_4=1',
            }

            params = (
                ('file', anime_id), # use custom id
                ('sendFile', 'true'),
                ('token', token), # use custom token
            )

            #response = requests.get('https://www.yourupload.com/download', headers=headers, params=params)

            src = src + "&sendFile=true&token=234c"
##            src = soup.find("meta", attrs={"property":"og:video"}).get("content")
##            src = src.replace(":8161/",":8161/play/")
            download_src["yourupload.com"] = src
            
        elif "streamango.com" in src:
            pass
        else:
            c += 1
            download_src["Unknown"+str(c)]= src
            
    return download_src
    

def collect_sources(url):

    unprepared_src = probe_sources(url)

    prepared_src = prepare_sources(unprepared_src)

    direct_src = final_sources(prepared_src)

    return direct_src

video_url = 'https://www16.kickassanime.io/anime/one-punch-man-982833/episode-01-709741'

sources = collect_sources(video_url)


print(sources)
