
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
import time


#incharge of cloning a specific game/board
class CloneGame:

    # gets: current game data = {"name": XXX, "size_x": YYY, "size_y": ZZZ, "url": TTT}
    # returns:-
    # action:init web drivers + gets website data
    def __init__(self,gameData):
        #data received from title
        self.gameData = gameData

        #download data && extract data
        driver = webdriver.PhantomJS()
        driver.get(self.gameData["url"])
        time.sleep(3)

        self.pageData = driver.find_element_by_id("board").get_attribute('innerHTML')
        driver.close()

        #get all of the board data
        self.getAllBoardData()


    # gets:-
    # returns:-
    # action: extract from web && creates list of data for current game
    def getAllBoardData(self):
        #extract data
        soup = BeautifulSoup(self.pageData)
        allGamesHTML = soup.findAll('td', attrs={'class':'nonogramsDef'})

        #run on all data
        self.boardData = list()
        for currentRow in allGamesHTML:
            #get content
            currentRowData = str(currentRow).split("<strong>")
            currentRowData = currentRowData[1].split("</strong>")
            currentRowData = currentRowData[0]

            #try getting as <br /> -------------------------------> for col titles
            currentRowNums = currentRowData.split("<br />")
            if len(currentRowNums) != 1:
                currentNumbers = currentRowNums[1:]

            # try spliting by  &nbsp; ------------------------------> for row titles
            else:
                currentRowNums = currentRowData.split(" &nbsp;")
                currentNumbers = currentRowNums[1:]

            #add data
            self.boardData.append(currentNumbers)


    # gets: -
    # returns:-
    # action: saves to file the current board with my format
    def startCloneGame(self):
        #create size format
        size = str(self.gameData["size_y"]) + " " + str(self.gameData["size_x"]) + " "

        #insert game size
        target = open("games/tempGame.txt", 'w')
        target.truncate()

        #insert size
        target.write(size)
        target.write("\n")


        #insert game
        counter = 0
        for currentRow in self.boardData:
            #set of numbers
            currentString = ""
            for number in currentRow:
                currentString += number + " "

            currentString = currentString[:-1]

            #add to view
            target.write(currentString)

            #add new lines to all except last
            if counter != len(self.boardData) -1:
                target.write("\n")

            counter +=1


        #close file writer
        target.close()

