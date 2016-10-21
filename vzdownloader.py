#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
# Internal
from urllib.request import urlopen
import threading
# External
import configparser
import colorama
import pdflib

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

# Get number of songs from site
line = urlopen("http://www.velkyzpevnik.cz/zpevnik").readlines()[22].decode('utf-8')
songCount = int(line[line.find("<b>")+4:][:line[line.find("<b>")+4:].index(" ")])
songsPercent = songCount;

pageIndex = 0
while (songCount):
    song = urlopen("http://www.velkyzpevnik.cz/song_print.php?id=" + str(pageIndex))
    songString = song.read().decode('utf-8')
    if not "<title> - </title>" in songString:
        songString = patchFile(songString)
        songFile = open("data/" + str(pageIndex) + ".html", "w", encoding="utf8")
        songFile.write(songString);
        songFile.close()
        songCount -= 1
    song.close()
    pageIndex += 1
    #print((songsPercent + 1 - songCount) / (songsPercent / 100))
