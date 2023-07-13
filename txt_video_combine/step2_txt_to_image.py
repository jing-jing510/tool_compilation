import base64
import json
import os

import chardet
import requests

# from requests import post
from requests.adapters import HTTPAdapter
from urllib3 import Retry

session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)
def save_img(b64_image, path):
    with open(path, "wb") as file:
        file.write(base64.b64decode(b64_image))

def post(url, data):
    return session.post(url, json=data)
def get_cloud_address():
    config_file = 'config.json'

    data = None

    if os.path.exists(config_file):
        with open(config_file, 'rb') as f:
            raw_data = f.read()
            # 确定编码 自配
            detected_encoding = chardet.detect(raw_data)['encoding']
        with open(config_file, 'r', encoding=detected_encoding) as f:
            config = json.load(f)
            cloud_address = config.get('cloud_address')
            # more_details = config.get('more_details')
            data = config.get('data')

    if data is None:
        data = {}
    # print(data)
    return data


def run_program():
    cloud_address = 'http://127.0.0.1:7861/sdapi/v1/txt2img'
    prompt = "mysterious figure in a dimly lit room, (silhouette:1.1), (vintage atmosphere:1.2), ancient wooden desk, sparse candlelight, faint moonlight filtering through the windows, (atmospheric lighting:1.2), black cloak, (billowing:1.1), adorned with a silent and enigmatic mask, (intricately designed:1.2), delicate fingers caressing an old and weathered parchment, [mysterious symbols] and hauntingly beautiful calligraphy filling the page, (ancient scroll:1.1), (elaborate calligraphy:1.2), (meticulous details:1.1), adjacent to the desk, an antique telescope, (adorned with gemstones:1.2), (subtle shimmer:1.1), a massive book, (meticulously illustrated:1.2), (mysterious symbols:1.1), (esoteric notations:1.1), beyond the window, a magnificent night view, (city skyline:1.2), (vast grasslands:1.1), (starry sky:1.2), stars glistening like diamonds on the ground, (serene atmosphere:1.2), (mystical aura:1.1), conveying a sense of otherworldly power, (intriguing:1.2), (hidden abilities:1.1), an aura of reverence and curiosity, pondering the mysteries of human existence, (unveil the secrets of life and death:1.2), unfathomable destiny, (uncanny power:1.1)"
    # data
    data = get_cloud_address()
    # 存储image_dir
    image_dir = 'image'
    data['prompt'] = prompt
    # print(data)
    # output_filev
    output_file = 'output1.png'

    response = post(cloud_address, data)
    if response.status_code == 200:
        print(response.json())
        save_img(response.json()['images'][0], os.path.join(image_dir,output_file))
    else:
        print(f'错误：{response.status_code}')


if __name__ == '__main__':
    run_program()
    # get_cloud_address()
    # save_img('F:\Midjourney\老人\1.png','image/output.png')