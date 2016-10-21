#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
# Internal
from urllib.request import urlopen
import argparse
import datetime
import glob
import os
# External
import colorama
import pdfkit
from natsort import natsorted

# Define constants
DATA_DIR = "data/"

# Define functions
def patchFile(string):
    # Fix head
    string = string.replace('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '<!doctype html>')
    string = string.replace('<html xmlns="http://www.w3.org/1999/xhtml" lang="cs">', '<html>')
    string = string.replace('<meta http-equiv="content-type" content="text/html;charset=UTF-8"/>', '<meta charset="UTF-8">')

    # Disable print dialog
    string = string.replace('<body onload="window.print()">', '<body>')

    # Remove AD in bottom
    string = string.replace("<p class='footer'>Další texty písniček s akordy najdete na serveru <b>http://www.velkyzpevnik.cz</b></p>", '')
    string = string.replace(".footer { padding-top:1em; border-top:1px solid black; font-size:9pt; text-align:center; }", '')

    return string

# Init colors
colorama.init();

# Print logo
print(colorama.Fore.YELLOW + " _____ _____ " + colorama.Fore.WHITE + "   ____                _           _         ")
print(colorama.Fore.YELLOW + "|  |  |__   |" + colorama.Fore.WHITE + "  |    \ ___ _ _ _ ___| |___ ___ _| |___ ___ ")
print(colorama.Fore.YELLOW + "|  |  |   __|" + colorama.Fore.WHITE + "  |  |  | . | | | |   | | . | .'| . | -_|  _|")
print(colorama.Fore.YELLOW + " \___/|_____|" + colorama.Fore.WHITE + "  |____/|___|_____|_|_|_|___|__,|___|___|_|  ")

# Argument parser
# Setup
argparser = argparse.ArgumentParser(description="Tool for creating song-book from velkyzpevnik.cz")
# Arguments
argparser.add_argument("--build", dest="build", action="store_const", const=True, default=False, help="Build song database")
argparser.add_argument("--rebuild", dest="rebuild", action="store_const", const=True, default=False, help="Rebuild song database")
argparser.add_argument("--delete", dest="rebuild", action="store_const", const=True, default=False, help="Delete song database")
# Parse arguments
args = argparser.parse_args()


# Get number of songs from site
line = urlopen("http://www.velkyzpevnik.cz/zpevnik").readlines()[22].decode('utf-8')
songCount = int(line[line.find("<b>")+4:][:line[line.find("<b>")+4:].index(" ")])
songsRemaining = songCount - len(glob.glob(DATA_DIR + '*.html'))
songsPercent = songCount;

# Get number of last index + 1
pageIndex = int(os.path.splitext(os.path.basename(natsorted(glob.glob(DATA_DIR + '*.html'))[-1]))[0]) + 1
while (songsRemaining):
    song = urlopen("http://www.velkyzpevnik.cz/song_print.php?id=" + str(pageIndex))
    songString = song.read().decode('utf-8')
    if not "<title> - </title>" in songString:
        songString = patchFile(songString)
        songFile = open(DATA_DIR + str(pageIndex) + ".html", "w", encoding="utf8")
        songFile.write(songString);
        songFile.close()
        songsRemaining -= 1
    song.close()
    pageIndex += 1
    print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "] " + str((songsPercent - songsRemaining) / (songsPercent / 100)))
