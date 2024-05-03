import requests
import os
from datetime import datetime, timedelta

def download_bing_images():
    base_url = "https://www.bing.com/HPImageArchive.aspx"
    output_dir = "/<mountpoint>/pictures/Bing"
    resolution = "1920x1080"
    markets = ["en-US"]
    #Optional Market options, enable or disable as needed
    #markets = ["en-US", "zh-CN", "ja-JP", "de-DE", "en-AU", "en-UK", "fr-FR", "en-CA"]

    unique_names = set()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for market in markets:
        for i in range(8):  # Last 8 days
            params = {
                "format": "js",
                "idx": i,
                "n": 1,
                "mkt": market
            }
            response = requests.get(base_url, params=params)
            data = response.json()

            if data['images']:
                image_data = data['images'][0]
                image_url = "https://www.bing.com" + image_data['urlbase'] + "_" + resolution + ".jpg"
                #image_name = image_data['startdate'] + "_" + image_data['title'].replace(' ', '_') + ".jpg"
                image_name = image_data['startdate'][:4] + "-" + image_data['startdate'][4:6] + "-" + image_data['startdate'][6:] + "_" + image_data['title'].replace(' ', '_') + ".jpg"
                if image_name not in unique_names:
                    unique_names.add(image_name)
                    image_path = os.path.join(output_dir, image_name)
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        with open(image_path, 'wb') as f:
                            f.write(image_response.content)
                        print(f"Downloaded {image_name}")

download_bing_images()
