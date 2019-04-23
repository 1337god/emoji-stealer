#!/usr/bin/env python3
import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.request import urlretrieve
import subprocess

def read_api(api_url):
    req = Request(api_url, headers={"User-Agent": 'Mozilla/5.0'})
    data = json.loads(urlopen(req).read().decode())
    return data

def download_emojis(json):
    print("The script will automatically append them to an emoji.txt file if you ever want to add them to your pleroma instance.")
    #happy, /emoji/custom/happy.png
    all_files = []
    emoji_file= open("emoji.txt","a")
    for emoji in json:
        file_extension = emoji["static_url"].split("/")
        file_extension = file_extension[-1].split("?")
        file_extension = file_extension[0].split(".")
        print("Downloading: " + emoji["shortcode"] + "." + file_extension[1])
        urlretrieve (emoji["static_url"], "./" + emoji["shortcode"] + "." + file_extension[1])
        emoji_file.write(emoji["shortcode"] + ", /emoji/custom" + emoji["shortcode"] + "." + file_extension[1] + "\n")
        all_files.append(emoji["shortcode"] + "." + file_extension[1])
    emoji_file.close()
    answer = input("Do you want me to move them to the right directory for you?(y/n)")
    if answer == "y":
        print("I'm assuming pleroma is in /opt/pleroma/, and that you are using the Static Directory in the default location (instance/static/) as the tutorial suggests.")
        if os.path.isdir("/opt/pleroma/instance/static/emoji/custom"):
            for f in all_files:
                os.rename(f, "/opt/pleroma/instance/static/emoji/custom" + f)
        else:
            print("Directory doesn't exist, exiting...")
            exit(0)
    else:
        print("Ok, I'm done here,goodbye!")
        exit(0)

def treat_url(instance_url):
    api_url = instance_url + "/api/v1/custom_emojis"
    return api_url


def main():
    instance_url = None
    try:
        instance_url = sys.argv[1]
    except IndexError:
        print("You need to specify a url.")
        exit(0)
    api_url = treat_url(instance_url)
    api_data = read_api(api_url)
    download_emojis(api_data)


main()
