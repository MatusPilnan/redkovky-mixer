import os
import random
import re
import sys
import getopt
import mp3_tagger
import time
import traceback

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
    subory = os.listdir(cesta)
    subory.sort()
    subory.pop(0)
    random.seed(n)
    random.shuffle(subory)
    i = 1
    zoznam = '''---
layout: default
title: Playlist Bárjaké reďkovky
---
# Bárjaké reďkovky


Toto je aktuálna forma playlistu Bárjaké reďkovky z dňa %s:  

*Nultý (000) sondžik je ako vždy Bon Jovi - You Give Love a Bad Name*  
''' % time.asctime(time.localtime(time.time()))
    for s in subory:
        if s == "barjake_redkovky.md":
            continue

        try:
            mp3 = mp3_tagger.MP3File(cesta + "\\" + s, )
            mp3.set_version(mp3_tagger.VERSION_2)
            try:
                tagy = mp3.get_tags()
            except AttributeError:
                tagy = {'artist': mp3.artist, 'song': mp3.song}

            if 'artist' not in tagy or 'song' not in tagy:
                print("Chybajuce tagy v subore " + s)
            try:
                umelec = str(tagy['artist']).strip()
            except KeyError:
                if oprav_chybajuce:
                    print("Zadaj novy nazov umelca: ")
                    umelec = input()
                    mp3.artist = umelec
                    mp3.save()
            try:
                nazov = str(tagy['song'])
            except KeyError:
                if oprav_chybajuce:
                    print("Zadaj novy nazov piesne: ")
                    nazov = input()
                    mp3.song = nazov
                    mp3.save()

            if umelec[-1] == '\0':
                umelec = umelec[:-1]
            if nazov[-1] == '\0':
                nazov = nazov[:-1]

            zoznam += (("%d. **" % i) + umelec + "** - " + nazov + "\n")
            print(re.sub("^[^a-zA-Z]*", "{0:0=3d}".format(i) + "_", s))
            os.rename(cesta + "\\" + s, cesta + "\\" + re.sub("^[^a-zA-Z]*", "{0:0=3d}".format(i) + "_", s))
            i += 1
        except mp3_tagger.MP3OpenFileError:
            print("CHYBA: %d bohuzial nie je .mp3" % i)
        except (UnicodeDecodeError, AttributeError) as e:
            print(e)
            zoznam += (("%d. " % i) + s + "\n")
            i += 1

    print("Pouzity seed: " + str(n))
    zoznam += ('''

Použitý seed: ```%d```
''' % int(n))
    zoznam_md = open(cesta + "/barjake_redkovky.md", "w", encoding="utf-8")
    zoznam_md.write(zoznam)
    zoznam_md.close()


if __name__ == "__main__":
    main(sys.argv[1:])
