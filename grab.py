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
# You may also need to install requests and lmxl            #
# $ pip install requests                                    #
# $ pip install lxml                                        #
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
# As said, this is a quick & dirty script that does the job #
# (as of today, of course ask.fm may change their website   #
# structure later so that this script has to be adapted)    #
#                                                           #
# (Almost) no exception or error handling has been          #
# implemented yet, this may be added in later versions.     #
#                                                           #
#############################################################

#############################################################
# Version 1.0 (01-May-2018)
# by LordOfTheSnow
# GitHub: https://github.com/LordOfTheSnow/AskFM-Grabber
#
# published under GNU General Public License v3.0
# see https://choosealicense.com/licenses/gpl-3.0/
#
# Please ensure that you have the right to grab something from a website with this script
# I do not take any legal responsibilities for a misuse of this script
#############################################################


# do some imports
import requests
import bs4
import sys
import urllib.request
import datetime
import time

# ask.fm pages usually contain all sorts of unicode images that interfer
# with things you might want to do later (i.e. build a wordcloud out of the
# text files), so they are removed here
#
# create translation map for non-bmp charactes
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


# change the name of the ask.fm-account you would like to grab
askURL = 'https://ask.fm' # base URL, do not change
askURI = '/OfficialClaireH'

# delay grabbing of next page to prevent potential blocking by ask.fm
# value is in seconds
delay = 2

#set up some constants and variables
filenamePrefix=askURI[1:]
filenameTimestamp = datetime.datetime.today().strftime('_%Y%m%d_%H%M%S')
filenameQuestions = filenamePrefix + filenameTimestamp + "_questions.txt"
filenameAnswers = filenamePrefix + filenameTimestamp + "_answers.txt"
filenameQandA = filenamePrefix + filenameTimestamp + "_q_and_a.txt"
numberOfImagesSaved = 0
numberOfQuestions = 0
numberOfAnswers = 0
numberOfPages = 0

#open output files
fileQuestions = open (filenameQuestions, "w", encoding='utf-8')
fileAnswers = open (filenameAnswers, "w", encoding='utf-8')
fileQandA = open (filenameQandA, "w", encoding='utf-8')

print ("now grabbing q+a from " + askURL + askURI)
print ("-----------------------------------------------------------------")

#loop while there still are "next" pages
while (askURI):
    time.sleep(delay)
    res = requests.get(askURL + askURI)

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    articles = soup.find_all("article")

    for article in articles:

        # get the question
        header = article.header
        h2 = header.h2
        question = h2.get_text("|", strip=True).translate(non_bmp_map)

        # convert to latin-1 to remove all stupid unicode characters
        # you may want to adapt this to your personal needs
        #
        # for some strange reason I have to first transform the string to bytes with latin-1
        # encoding and then do the reverse transform from bytes to string with latin-1 encoding as
        # well... maybe has to be revised later
        bQuestion = question.encode('latin-1', 'ignore')
        question = bQuestion.decode('latin-1', 'ignore')
        numberOfQuestions += 1
        
        print ("Question: " + question)
        fileQuestions.write("{}\n".format(question))
        fileQandA.write("{}\n".format(question))
        
        # get the answer
        content=""
        streamItemContent = article.select('.streamItem_content')
        if (len(streamItemContent)):
            if (len(streamItemContent[0].contents) > 1):
                # remove last item of content list as it only contains a 'more...' link
                #del streamItemContent[0].contents[len(streamItemContent[0].contents)-1]
                streamItemContent[0].contents.pop()

                content = str(streamItemContent[0].get_text("|", strip=True)).translate(non_bmp_map)

                # for whatever reasons, sometimes the "View more" text is still there,
                # so remove it here once and forever
                content = content.replace("|View more", "")
                
            if (len(streamItemContent[0].contents) == 1):
                content = str(streamItemContent[0].contents[0]).translate(non_bmp_map)

            # convert to latin-1 to remove all stupid unicode characters
            # you may want to adapt this to your personal needs
            #
            # for some strange reason I have to first transform the string to bytes with latin-1
            # encoding and then do the reverse transform from bytes to string with latin-1 encoding as
            # well... maybe has to be revised later
            bContent = content.encode('latin-1', 'ignore')
            content = bContent.decode('latin-1', 'ignore')
            numberOfAnswers += 1
            
            print ("Answer  : " + content + "\n")
            fileAnswers.write("{}\n".format(content))
            fileQandA.write("{}\n\n\n".format(content))


        # maybe there is an image?
        streamItemVisual = article.select('.streamItem_visual')
        if (len(streamItemVisual)):
            link = streamItemVisual[0].find('a')
            visual = link.get('data-url')

            if visual:
                print ("Visual : " + visual + "\n")
                localFilename = (filenamePrefix + "_{0:04d}_".format(numberOfImagesSaved) +
                                 visual.split('/')[-1])
                try:
                    urllib.request.urlretrieve(visual, localFilename)
                    numberOfImagesSaved +=1
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                

    # find the link to the next page
    pageNext = soup.select('.item-page-next')

    if (len(pageNext)):
        # only continue if next link is found    
        print ('================================= page ' + str (numberOfPages+1)
               + " (q: " + str(numberOfQuestions) + ", a: "
               + str(numberOfAnswers) + ", i: " + str(numberOfImagesSaved) + ")")
        askURI = pageNext[0].get('href')
        numberOfPages +=1
    else:
        askURI = ''

#uncomment the following line to stop after one page
#    askURI = ''

#close all opened files
fileQandA.close()
fileQuestions.close()
fileAnswers.close()

#output some results        
print ("number of questions   : " + str(numberOfQuestions))
print ("number of answers     : " + str(numberOfAnswers))
print ("number of saved images: " + str(numberOfImagesSaved))

