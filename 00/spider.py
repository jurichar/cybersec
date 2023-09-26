# This program is used to scrape every image from the website recursively.

import os
import re
import argparse
import requests
import bs4
from urllib.parse import urljoin

def inputLineParser(): # parse the input line
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

def downloadImage(url, path): # url is the url of the image, path is the path to save the image
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

def scrapeWebsite(url, path, visited, depth=1, max_depth=5):
    if depth > max_depth:
        return

    visited.add(url)
    
    try:
        response = requests.get(url)
    except Exception as e:
        print(f'Failed to get content of {url}')
        return
    
    if response.status_code != 200:
        print(f'Failed to get content of {url}')
        return

    soup = bs4.BeautifulSoup(response.text, 'html.parser') # html.parser is the default parser

    img_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    for img_tag in soup.find_all('img'): # find_all() returns a list
        img_url = img_tag.get('src')
        if img_url is None:
            continue
        if any(ext in img_url for ext in img_formats):
            print(f'Found image: {img_url}')
            # downloadImage(img_url, path)

    if args.recursive and depth < max_depth:
        for anchor_tag in soup.find_all('a'):
            anchor_url = anchor_tag.get('href')
            if anchor_url:
                anchor_url = urljoin(url, anchor_url)
                if not re.match(r'^https?://', anchor_url):
                    continue
                if anchor_url not in visited:
                    scrapeWebsite(anchor_url, path, visited, depth+1 , max_depth)

if __name__ == '__main__':
    args = inputLineParser()
    visited = set()
    scrapeWebsite(args.url, args.path, visited, 1, args.level)
    # scrapeWebsite("https://www.woopets.fr/chien/races/", "./data/", visited, 1, 2)
