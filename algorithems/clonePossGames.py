

from selenium import webdriver
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin
import time
import random


#incharge of cloning list of possible games to solve
class ClonePosGames:
    allGamesList = list()

    # gets:-
    # returns:-
    # action:init web drivers + gets website data
    def __init__(self):

        #get data from site
        self.url = 'http://www.goobix.com/games/nonograms/?s=-'

        #init driver
        self.driver = webdriver.PhantomJS()

        #get data from link
        self.driver.get(self.url)
        time.sleep(1)
        self.extractData()

    # gets:-
    # returns:-
    # action: close web driver at the end of program
    def __del__(self):
        self.driver.close()

    # gets:-
    # returns:-
    # action:creates list of possible games with their data
    def extractData(self):
        #get main data section
        pageData = self.driver.find_element_by_id("drawings").get_attribute('innerHTML')

        # extract data
        soup = BeautifulSoup(pageData)
        allGamesHTML = soup.findAll('div', attrs={'style': 'width:40px;margin:20px;display:inline-block'})

        # turn to lists
        self.allGamesList = list()

        counter = 1
        for currentGameHTML in allGamesHTML:
            # get link
            linkData = str(currentGameHTML).split("<a href=\"")
            linkData = linkData[1].split("\"")
            linkData = linkData[0]
            linkData = urljoin(self.url, linkData)

            # get size
            sizeData = str(currentGameHTML).split("<br />")
            sizeData = sizeData[1].split("</a>")
            sizeData = sizeData[0]
            sizeData = sizeData.split("x")

            # append data
            gameName = "game " + str(counter)
            self.allGamesList.append({"name": gameName, "size_x": sizeData[0], "size_y": sizeData[1], "url": linkData})
            counter += 1


    # gets:-
    # returns:-
    # action:clickes the "next" button in driver, and makes the range of sizes of boards bigger
    def biggerBoards(self):
        self.driver.find_element_by_id("next").click()
        time.sleep(1)
        self.extractData()

    # gets:-
    # returns:-
    # action:clickes the "prev" button in driver, and makes the range of sizes of boards smaller
    def smallerBoards(self):
        self.driver.find_element_by_id("prev").click()
        time.sleep(1)
        self.extractData()

    # gets:-
    # returns:-
    # action:return ten random boards from list
    def returnPosGames(self):
        onlyTenBoards = self.allGamesList[:]
        random.shuffle(onlyTenBoards)

        return onlyTenBoards[:10]