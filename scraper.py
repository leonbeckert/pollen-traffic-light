#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
from bs4 import BeautifulSoup
import requests
import time
import serial

#with open('sample.html') as html_file:
    #soup = BeautifulSoup(html_file, 'lxml')
    #print(soup.prettify())

ampel = 0
firstRunBool = 1
ser = serial.Serial('/dev/ttyACM0', 9600)
url = 'https://www.wetteronline.de/pollen?gid=10866&lat=48.133&locationname=M%C3%BCnchen&lon=11.567'
#stadt = ""

bools = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
strings = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

def firstRun():
    print("Bitte geben Sie nun an, welche Allergien Sie haben")
    erleInput = input("Erle? (y/n)")
    if erleInput == "y" or erleInput == "yes":
        bools[0] = 1
    haselInput = input("Hasel? (y/n)")
    if haselInput == "y" or haselInput == "yes":
        bools[1] = 1
    pappelInput = input("Pappel? (y/n)")
    if pappelInput == "y" or pappelInput == "yes":
        bools[2] = 1
    weideInput = input("Weide? (y/n)")
    if weideInput == "y" or weideInput == "yes":
        bools[3] = 1
    ulmeInput = input("Ulme? (y/n)")
    if ulmeInput == "y" or ulmeInput == "yes":
        bools[4] = 1
    birkeInput = input("Birke? (y/n)")
    if birkeInput == "y" or birkeInput == "yes":
        bools[5] = 1
    bucheInput = input("Buche? (y/n)")
    if bucheInput == "y" or bucheInput == "yes":
        bools[6] = 1
    ampferInput = input("Ampfer? (y/n)")
    if ampferInput == "y" or ampferInput == "yes":
        bools[7] = 1
    roggenInput = input("Roggen? (y/n)")
    if roggenInput == "y" or roggenInput == "yes":
        bools[8] = 1
    graeserInput = input("Graeser? (y/n)")
    if graeserInput == "y" or graeserInput == "yes":
        bools[9] = 1
    eicheInput = input("Eiche? (y/n)")
    if eicheInput == "y" or eicheInput == "yes":
        bools[10] = 1
    wegerichInput = input("Wegerich? (y/n)")
    if wegerichInput == "y" or wegerichInput == "yes":
        bools[11] = 1
    beifussInput = input("Beifuss? (y/n)")
    if beifussInput == "y" or beifussInput == "yes":
        bools[12] = 1
    ambrosiaInput = input("Ambrosia? (y/n)")
    if ambrosiaInput == "y" or ambrosiaInput == "yes":
        bools[13] = 1

def crawl():
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, "lxml")

    erle = str(soup.find(id="Erl_text").find_next())
    strings[0] = erle.split('"', 4)[3]

    hasel = str(soup.find(id="Has_text").find_next())
    strings[1] = hasel.split('"', 4)[3]

    pappel = str(soup.find(id="Pap_text").find_next())
    strings[2] = pappel.split('"', 4)[3]

    weide = str(soup.find(id="Wed_text").find_next())
    strings[3] = weide.split('"', 4)[3]

    ulme = str(soup.find(id="Ulm_text").find_next())
    strings[4] = ulme.split('"', 4)[3]

    birke = str(soup.find(id="Bir_text").find_next())
    strings[5] = birke.split('"', 4)[3]

    buche = str(soup.find(id="Buc_text").find_next())
    strings[6] = buche.split('"', 4)[3]

    ampfer = str(soup.find(id="Zur_text").find_next())
    strings[7] = ampfer.split('"', 4)[3]

    roggen = str(soup.find(id="Rog_text").find_next())
    strings[8] = roggen.split('"', 4)[3]

    graeser = str(soup.find(id="Gra_text").find_next())
    strings[9] = graeser.split('"', 4)[3]

    eiche = str(soup.find(id="Eic_text").find_next())
    strings[10] = eiche.split('"', 4)[3]

    wegerich = str(soup.find(id="Wee_text").find_next())
    strings[11] = wegerich.split('"', 4)[3]

    beifuss = str(soup.find(id="Bij_text").find_next())
    strings[12] = beifuss.split('"', 4)[3]

    ambrosia = str(soup.find(id="Amb_text").find_next())
    strings[13] = ambrosia.split('"', 4)[3]

def running():
    status = 0 #1 for green 2 for yellow 3 for red
    for i in range(0, 14):
        if bools[i] == 1:
            if strings[i] == "weakburden" and status < 2:
                status = 1
            elif strings[i] == "moderateburden" and status < 3:
                status = 2
            elif strings[i] == "strongburden":
                status = 3
    if status > 0:
        if status == 1:
            ser.write(b'1')
        elif status == 2:
            ser.write(b'2')
        elif status == 3:
            ser.write(b'3')
    else:
        ser.write(b'1')

if firstRunBool:
    firstRun()
    firstRunBool = 0
    crawl()
    for i in range(0, 12):
        if(i % 10 == 0):
            crawl()
        running()
        time.sleep(1)
