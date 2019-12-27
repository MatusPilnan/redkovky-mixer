import getopt
import glob
import os
import random

import jinja2
import mp3_tagger
import sys
import time
from jinja2 import Environment

from config import *
from song import Song


def get_filenames(path='', extension='.mp3'):
    if path[-1] == '/' or path[-1] == '\\':
        path = path + '*' + extension
    elif len(path) > 0:
        path = path + '/*' + extension

    filenames = glob.glob(pathname=path)
    result = [filename for filename in filenames]
    result.sort()
    return result


def main(argv):
    cesta = os.getcwd()
    n = random.randrange(sys.maxsize)
    oprav_chybajuce = True

    try:
        opts, args = getopt.getopt(argv, "hp:s:f", ["help", "priecinok=", "seed="])
    except getopt.GetoptError:
        print('main.py [-p <priecinok>] [-s <seed>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py [-p <priecinok>] [-s <seed>]')
            sys.exit()
        elif opt in ("-p", "--priecinok"):
            print(arg)
            cesta = arg
        elif opt in ("-s", "--seed"):
            n = arg
        elif opt in ("-f",):
            oprav_chybajuce = False

    print(cesta)
    print(n)
    subory = get_filenames(cesta)
    subory.pop(0)
    random.seed(n)
    random.shuffle(subory)
    i = 1
    songs = []
    for s in subory:
        try:
            song = Song(s)
            song.update_file_position(i)
            songs.append(song)
            i += 1
        except mp3_tagger.MP3OpenFileError:
            print("CHYBA: %d bohuzial nie je .mp3" % i)
        except (UnicodeDecodeError, AttributeError) as e:
            print(e)
            i += 1

    template_env = Environment(loader=jinja2.loaders.FileSystemLoader(TEMPLATE_FOLDER))
    template = template_env.get_template(TEMPLATE_NAME)
    template.stream(songs=songs, seed=n, time=str(time.asctime(time.localtime(time.time())))).dump(
        cesta + "/barjake_redkovky.md")


if __name__ == "__main__":
    main(sys.argv[1:])
