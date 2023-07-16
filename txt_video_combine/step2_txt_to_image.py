import base64
import csv
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

def convert_to_utf8(filename):
    # determine the file encoding
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())

    original_encoding = result['encoding']

    # read the file with original encoding
    with open(filename, 'r', encoding=original_encoding) as f:
        contents = f.read()

    # write the file with utf-8 encoding
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(contents)

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


def run_program_test():
    cloud_address = 'http://127.0.0.1:7861'
    url = cloud_address.rstrip('/') + '/sdapi/v1/txt2img' if cloud_address else ""
    prompt = "mysterious figure in a dimly lit room, (silhouette:1.1), (vintage atmosphere:1.2), ancient wooden desk, sparse candlelight, faint moonlight filtering through the windows, (atmospheric lighting:1.2), black cloak, (billowing:1.1), adorned with a silent and enigmatic mask, (intricately designed:1.2), delicate fingers caressing an old and weathered parchment, [mysterious symbols] and hauntingly beautiful calligraphy filling the page, (ancient scroll:1.1), (elaborate calligraphy:1.2), (meticulous details:1.1), adjacent to the desk, an antique telescope, (adorned with gemstones:1.2), (subtle shimmer:1.1), a massive book, (meticulously illustrated:1.2), (mysterious symbols:1.1), (esoteric notations:1.1), beyond the window, a magnificent night view, (city skyline:1.2), (vast grasslands:1.1), (starry sky:1.2), stars glistening like diamonds on the ground, (serene atmosphere:1.2), (mystical aura:1.1), conveying a sense of otherworldly power, (intriguing:1.2), (hidden abilities:1.1), an aura of reverence and curiosity, pondering the mysteries of human existence, (unveil the secrets of life and death:1.2), unfathomable destiny, (uncanny power:1.1),1boy, goat beard, white hair, suit"
    # data
    data = get_cloud_address()
    # 存储image_dir
    image_dir = 'image'
    data['prompt'] = prompt
    # print(data)
    # output_filev
    output_file = 'output1.png'

    response = post(url, data)
    if response.status_code == 200:
        print(response.json())
        save_img(response.json()['images'][0], os.path.join(image_dir,output_file))
    else:
        print(f'错误：{response.status_code}')
def run_program_with_args(config_path, prompt_path):
    convert_to_utf8(config_path)
    convert_to_utf8(prompt_path)
    # Load the config
    with open(config_path, 'rb') as f:
        raw_data = f.read()
    detected_encoding = chardet.detect(raw_data)['encoding']
    with open(config_path, 'r', encoding=detected_encoding) as f:
        config = json.load(f)

        cloud_address = config.get('cloud_address')

        if not cloud_address.startswith(('http://', 'https://')):
            cloud_address = 'http://' + cloud_address
        data = config.get('data')
    if data is None:
        data = {}

        # Load the prompt
    prompts = []
    with open(prompt_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)
        for row in csv_reader:
            prompts.append(row[2])  # Assuming the 3rd column contains the prompts
        # print(prompts)
     # Update the original run_program() function
    output_paths =run_program(cloud_address, data, prompts)
    return output_paths

def run_program_single_prompt(config_path, prompt, index):
    # Load the config
    with open(config_path, 'rb') as f:
        raw_data = f.read()
    detected_encoding = chardet.detect(raw_data)['encoding']
    with open(config_path, 'r', encoding=detected_encoding) as f:
        config = json.load(f)

    cloud_address = config.get('cloud_address')
    data = config.get('data')
    if data is None:
        data = {}

    # Run the program with a single prompt
    run_program(cloud_address, data, [prompt], index)
def run_program(cloud_address, data, prompts, index=1):
    url = cloud_address.rstrip('/') + '/sdapi/v1/txt2img' if cloud_address else ""
    image_dir = 'image'
    output_paths = []
    for i, prompt in enumerate(prompts, start=index):
        data['prompt'] = prompt
        # print(data)
        output_file = f'output{i}.png'
        output_path = os.path.join(image_dir, output_file)
        output_paths.append(output_path)
        print(output_paths)
        response = post(url, data)
        if response.status_code == 200:
            print(response.json())
            save_img(response.json()['images'][0], os.path.join(image_dir, output_file))
        else:
            print(f'错误：{response.status_code}')
    return output_paths
if __name__ == '__main__':
    # run_program()
    # run_program_test()
    run_program_with_args('config.json', 'novel/关键词.csv')
    # get_cloud_address()
    # save_img('F:\Midjourney\老人\1.png','image/output.png')