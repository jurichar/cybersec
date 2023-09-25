# This program is used to scrape every image from the website recursively.

import os
import argparse
import requests


def inputLineParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='The url of the website.')
    parser.add_argument('-r', '--recursive',
                        help='Recursively scrape the website.')
    parser.add_argument('-l', '--level', type=int, default=5,
                        help='The level of recursion.')
    parser.add_argument('-p', '--path', default="./data/",
                        help='The path to save the images.')
    args = parser.parse_args()
    return args


def downloadImage(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        img_name = os.path.basename(url)
        img_path = os.path.join(path, img_name)

        with open(img_path, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {img_name} to {img_path}')

    except Exception as e:
        print(f'Failed to download image from {url}.')


if __name__ == '__main__':
    downloadImage(
        'https://www.powertrafic.fr/wp-content/uploads/2023/04/image-ia-exemple.png', './data/')
    # args = inputLineParser()
    # print(args)
