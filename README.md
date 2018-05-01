# AskFM-Grabber
Python script to extract questions, answers and linked images from an ask.fm-account; uses BeautifulSoup for website scraping

#############################################################
# grab.py                                                   #
#                                                           #
# Quick & dirty straightforward Python3 script (no object-  #
# oriented programming so far) to grab questions, answers   #
# and uploaded images from an ask.fm account                #
#                                                           #
#                                                           #
# For website scraping, BeautifulSoup is used. Please make  #
# sure to install BeautifulSoup before running this script. #
#                                                           #
# $ pip install beautifulsoup4                              #
#                                                           #
#   see https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
#                                                           #
#                                                           #
# This script creates three text files:                     #
#  one for the questions                                    #
#  one for the answers                                      #
#  one for questions and answers together                   #
#                                                           #
# It will also try to download every image hat has been     #
# uploaded to ask.fm as an answer. Videos or linked images  #
# are not supported (yet(?)).                               #
#                                                           #
# All files will be placed in the current directory.        #
#                                                           #
# As said, this is a quick & dirty script that does the job.#
# (Almost) no exception or error handling has been          #
# implemented yet, this may be added in later versions.     #
#                                                           #
#############################################################

# Version 1.0 (01-May-2018)
# by LordOfTheSnow
# GitHub: https://github.com/LordOfTheSnow/AskFM-Grabber
