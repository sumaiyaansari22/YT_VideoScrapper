from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import mysql.connector




def scroll_to_end(wd,sleep_between_interactions=1):
    wd.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(sleep_between_interactions)

def find_elements(wd,selector,attribute):
        elements = wd.find_elements(By.CSS_SELECTOR,selector)
        data = extractAttribute(elements,attribute)
        return data

'''def find_element(wd,selector,attribute):
    elements = wd.find_element(By.CSS_SELECTOR,selector)
    extractAttribute(elements,attribute)'''
def extractAttribute(elements,attribute):
    get = []
    if attribute == 'href' or attribute == 'src':
        for i in elements:
            get.append(i.get_attribute(attribute))
    elif attribute == 'text':
        for i in elements:
            get.append(i.text)
    return get

'''channelNames = ['@krishnaik06', '@HiteshChoudharydotcom', '@Telusko', '@saurabhexponent1']
def extractUrls(wd,channelNames,maxLinks = 1):

    urlList = {}
    for i in channelNames:
        urlList[i] = []

    currentLink = 0;
    #maxLinks =  1;
    for name in channelNames:
        wd.get(f"https://www.youtube.com/{name}/videos")
        while True:
            scroll_to_end(wd)
            urls =  find_elements(wd,'#video-title-link','href')
            thumbnail  = find_elements(wd,".yt-core-image--loaded",'src')
            title = find_elements(wd,"#video-title",'text')

            if len(urls)>=maxLinks and len(thumbnail)>=maxLinks:
                break
        #print(len(thumbnail))
        #print(likes)
        for i in range(len(urls)):
            if currentLink == maxLinks:
                break
            url = urls[i]
            thumbnails = thumbnail[i]
            videotitle = title[i]
            urlList[name].append([url,thumbnails,videotitle])

            currentLink += 1
        currentLink = 0
    return urlList

with webdriver.Chrome() as wd:
    urlList = extractUrls(wd,channelNames)
    #for i in urlList:
        #print(len(urlList[i]))
    for key in urlList:
        for details in urlList[key]:
            try:
                wd.get(details[0])
            #likes = WebDriverWait(wd,15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#segmented-like-button"))).text
                time.sleep(2)
                likes = find_elements(wd,"#segmented-like-button",'text')[0]
                commentCount = WebDriverWait(wd,15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".count-text"))).text.split(' ')[0]
            #print(commentCount)
                actualLen=0
                commName = 0
                while True:
                    scroll_to_end(wd)
                    actualComment = find_elements(wd,"#comment-content",'text')
                    commentorName = find_elements(wd,"#author-text",'text')
                #actualComment = wd.find_elements(By.CSS_SELECTOR,"#comment-content")
                #print(len(actualComment))

                    if commName == len(commentorName):
                    #print('hi')
                        break
                    commName = len(actualComment)
                #actualLen = len(actualComment)
                commentDetails = []
                for comm in range(len(actualComment)):
                    if actualComment[comm] == '':
                        continue
                    else:
                        actualComment[comm] = [actualComment[comm],commentorName[comm]]
                        commentDetails.append(actualComment[comm])
                details.append(commentDetails)
                details.append(likes)
                details.append(commentCount)
            except:
                print("Page not loaded",e)
                continue
    print(urlList)'''


def scrappe(video_url):

    with webdriver.Chrome() as wd:
        wd.get(video_url)
        time.sleep(10)
        vid_content = []
        title = find_elements(wd,"#title h1",'text')[0]
        likes = find_elements(wd, "#segmented-like-button", 'text')[0]
        commentCount = WebDriverWait(wd, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".count-text"))).text.split(' ')[0]
        actualLen = 0
        commName = 0
        while True:
            scroll_to_end(wd)
            actualComment = find_elements(wd, "#comment-content", 'text')
            commentorName = find_elements(wd, "#author-text", 'text')
            # actualComment = wd.find_elements(By.CSS_SELECTOR,"#comment-content")
            # print(len(actualComment))

            if commName == len(commentorName):
                # print('hi')
                break
            commName = len(actualComment)
        # actualLen = len(actualComment)
        commentDetails = []
        for comm in range(len(actualComment)):
            if actualComment[comm] == '':
                continue
            else:
                actualComment[comm] = [actualComment[comm], commentorName[comm]]
                commentDetails.append(actualComment[comm])
        vid_content.append(title)
        vid_content.append(likes)
        vid_content.append(commentCount)
        vid_content.append(commentDetails)

    return  vid_content

#res = scrappe('https://www.youtube.com/watch?v=mHQPzVse2oA')
#print(res)

def insert_values(obj):
    mydb = mysql.connector.connect(user='root', password='sumaiya22',
                                   host='localhost',
                                   database='assignment1')
    cursor = mydb.cursor()

    for keys in obj:
        for details in obj[keys]:

            insertQuery = (
                "insert into `yt_scrap` (`youtuber_name`, `video_link`, `likes`, `no_of_comments`, `title`, `thumbnail_link`)"
                "values("
                f" '{keys}','{details[0]}','{details[4]}','{details[5]}','{details[2]}','{details[1]}'"
                ")"
            )
            '''cursor.execute(cursor.execute(
                'insert into yt_scrap (youtuber_name, video_link, likes, no_of_comments, title, thumbnail_link)'
                f'values ("{keys}","{details[0]}","{details[4]}","{details[5]}","{details[2]}","{details[1]}")'
                ))'''
            cursor.execute(insertQuery)
            mydb.commit()
    cursor.close()

#insert_values();







