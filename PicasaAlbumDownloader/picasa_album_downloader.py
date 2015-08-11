#!/usr/bin/python3

"""picasa_album_downloader.py: Downloads all the images from a Picasa album."""

__author__ = 'andrei.muntean.dev@gmail.com (Andrei Muntean)'

import os.path
import re
import sys
from urllib.request import urlopen, urlretrieve

IMG_EXTENSIONS = ('.gif', '.jpg', '.png')


def get_input_destination():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print('Where would you like to download the images?')
    
        return input('> ')


def get_img_urls(url):
    response = urlopen(url, timeout=5)
    html = str(response.read())
    img_urls = []

    for extension in IMG_EXTENSIONS:
        for occurrence in re.finditer(extension, html.lower()):
            # Picasa uses " as the URL delimiter.
            delimiter = '"'

            # Gets the starting position of the URL.
            url_start = html[:occurrence.start()].rfind(delimiter) + 1

            # Gets the URL.
            img_url = html[url_start:occurrence.end()]

            # User-uploaded images have a unique 'Ic42/s128' tag. This skips all
            # the URLs which don't.
            if not 'Ic42/s128' in img_url:
                continue

            # The image resolution is represented by 's128'. Setting it to 's16383'
            # (2^14 - 1) will display the picture at its highest resolution.
            img_url = img_url.replace('Ic42/s128', 's16383-Ic42')

            # Stores the URL if it hasn't already been stored.
            if not img_url in img_urls:
                img_urls.append(img_url)
    
    return img_urls


def download(img_urls, destination):
    """Downloads the images from the given URLs into the specified destination."""
    
    if not os.path.exists(destination):
        print('Creating directory \'%s\'.' % destination)
        os.makedirs(destination)

    for img_url in img_urls:
        # Sets the image name as the string that follows the last '/' in the URL.
        img_name = img_url[img_url.rfind('/') + 1:]

        try:
            # Downloads the image into the specified folder.
            urlretrieve(img_url, os.path.join(destination, img_name))
            print('Downloaded \'%s\'.' % img_name)
        except:
            pass


def run():
    """Runs the program."""

    # The URL of a Picasa album.
    url = 'https://picasaweb.google.com/user-id/album-name'
    destination = get_input_destination()

    try:
        download(get_img_urls(url), destination)
        print('Download complete.')
    except:
        raise SystemExit('An error has occurred. Could not download images.')


if __name__ == '__main__':
    run()