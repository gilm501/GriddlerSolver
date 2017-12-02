from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label

from algorithems.griddlerSolver import GriddlerSolver
from designTemplate import designTemplate
from algorithems.clonePossGames import ClonePosGames
from algorithems.cloneGame import CloneGame

from functools import partial
import cPickle as pickle



#incharge of game board design and elements
class GameBoard(designTemplate):

    #init data
    def __init__(self,**kwargs):
        designTemplate.__init__(self)

        #getsGamesData-> holdes the object that handles possible boards to display
        #self.getGamesData = ClonePosGames()


        #start the view which presents possible boards to display
        #comment if wifi does not work
        #self.startGamesChoser()

        self.startTableView(None,None) # uncomment if wifi does not work


    #---------------------------------------------- PART OF - VIEW THAT DISPLAY POSSIBLE BOARDS TO SOLVE

    #gets:-
    #returns:-
    #action:clears the view and displayes possible boards to solve
    def reloadGames(self):
        self.clear_widgets()
        self.startGamesChoser()

    # gets:-
    # returns:-
    # action:changes the range of sizes of boards to smaller boards,
    #        clears the view and displayes possible boards to solve
    def smallerBoards(self):
        self.getGamesData.smallerBoards();
        self.reloadGames();

    # gets:-
    # returns:-
    # action:changes the range of sizes of boards to bigger boards,
    #        clears the view and displayes possible boards to solve
    def biggerBoards(self):
        self.getGamesData.biggerBoards();
        self.reloadGames();


    # gets:-
    # returns:-
    # action: displayes on view  possible games to solve view
    def startGamesChoser(self):
        boardData = self.initSelectGriddler()

        self.cols = 3
        self.addElements(boardData)


    # gets:-
    # returns: board data of possible games to solve view
    # action: -
    def initSelectGriddler(self):
        #get available possible game
        possibleGamesData = self.getGamesData.returnPosGames()

        #add widgets
        boardData = list()

        #add titleRow
        titleCell = Label(text="Gils griddler solver", font_size='30sp')

        boardData.append(Label(text="", font_size='20sp'))
        boardData.append(titleCell)
        boardData.append(Label(text="", font_size='20sp'))

        #add action buttons
        smallerBoards = Button(text="Smaller boards",on_press=lambda a : self.smallerBoards() )
        biggerBoards = Button(text="Bigger Boards",on_press=lambda a : self.biggerBoards())
        newGames = Button(text="load other boards",on_press=lambda a : self.reloadGames())

        boardData.append(smallerBoards)
        boardData.append(biggerBoards)
        boardData.append(newGames)


        #add all possible boards with design
        for currentGame in possibleGamesData:
            #init widgets
            currentTitleCell = Label(text=currentGame["name"], font_size='16sp')
            currentSize = Label(text=str(currentGame["size_x"]) + "*"+str(currentGame["size_y"]), font_size='16sp')

            currentGameCopy = pickle.loads(pickle.dumps(currentGame, -1))
            startGame = Button(text="Start",on_press=partial(self.startTableView, currentGameCopy))

            #add widgets to board
            boardData.append(currentTitleCell)
            boardData.append(currentSize)
            boardData.append(startGame)


        return boardData;






    #---------------------------------------------- PART OF - ACTUALL GAME/BOARD SOLVING

    # gets:-
    # returns:-
    # action: returnes to the view that displays games options to solve
    def backToMenuView(self):
        self.clear_widgets()
        self.startGamesChoser()


    # gets: the specific game/table that was clicked to solve, the button that was clicked
    # returns:-
    # action: changes to the current selected game view
    def startTableView(self, gameData,instace):
         #inserts current game to tempGame.txt
         #cloneGameHandler = CloneGame(gameData)
         #cloneGameHandler.startCloneGame()


         #load new game
         self.clear_widgets()

         # init design from temp file
         self.initFileData("game2.txt")
         self.cols = self.gameCols + 1

         #add elements to view
         self.addElements(self.returnBoardElements())



     # gets:file path to read
     # returns:-
     # action: saves current game rows and cols
    def initFileData(self,filePath):
        #read file
        self.filePath = "games/"+filePath

        currentFile = open(self.filePath,"r")

        self.fileData = currentFile.read()

        #get size of game
        lengthData = self.fileData.split(' ')

        #first rows -> second
        self.gameRows = int(filter(str.isdigit, lengthData[0]))
        self.gameCols = int(filter(str.isdigit, lengthData[1]))

        print lengthData
        print "rows : " , self.gameRows
        print "cols : ", self.gameCols



    # gets:-
    # returns:-
    # action: creates element of current game/board
    def returnBoardElements(self):
        #init data
        boardData = list()
        self.rowTitle = list()
        self.colTitle = list()
        self.cells = list()

        # add to title of titles
        currentCell = Label(text=str(self.gameRows) + "*" + str(self.gameCols), font_size='10sp', size_hint_y=None,
                            height=140)
        boardData.append(currentCell)


        # ADD COL TITLE
        currentTitle = 0

        titles = self.fileData.split('\n')
        titles = titles[1:]  # without size

        for row in xrange(self.gameCols):
            currentTitleText = titles[currentTitle].replace(" ", "\n")
            currentCell = Label(text=currentTitleText, font_size='10sp', size_hint_y=None, height=140)

            boardData.append(currentCell)
            self.rowTitle.append(currentCell)

            currentTitle += 1

        # ADD BOARD DATA
        for row in xrange(self.gameRows):
            # add row title
            currentCell = Label(text=titles[currentTitle], font_size='10sp', size_hint_x=None, width=140)
            currentTitle += 1

            boardData.append(currentCell)
            self.colTitle.append(currentCell)

            # add col cells
            for col in xrange(self.gameCols):
                currentCell = Button(text=" ", background_color=(5, 5, 5, 1))

                boardData.append(currentCell)
                self.cells.append(currentCell)


        # create start button
        startButton = Button(text="start solving", size_hint_x=None, width=200, size_hint_y=None, height=70,
                             on_press=lambda a: self.startSolving(a))
        boardData.append(startButton)


        # add line of spaces
        for col in xrange(self.gameCols):
            currentCell = Label(text=" ")

            boardData.append(currentCell)

        #create back button
        backButton = Button(text="Back", size_hint_x=None, width=200, size_hint_y=None, height=70,
                            on_press=lambda a: self.backToMenuView())

        boardData.append(backButton)

        return boardData;


    # gets:start button
    # returns:-
    # action: saves current game rows and cols
    def startSolving(self, button=None):
        button.disabled = True

        #start solving
        solver = GriddlerSolver(self.rowTitle, self.colTitle, self.cells, self.gameCols, self.gameRows)
        actionData = solver.solveGriddler()

        print actionData

        #display solution
        self.performSolutionAction(actionData, 0)


    # gets:total rows that need to be displayed, current cell index in row
    # returns:-
    # action: present solution on board
    def performSolutionAction(self, actionData, cellIndex):
        #if no action has been found
        if actionData == False:
            print "No solution"
            return;

        #if finished row, progress to next row
        if len(actionData[0]) == 0:
            actionData = actionData[1:]

        #if finished table stop
        if actionData == None or len(actionData) == 0 or actionData[0][0] == None:
            return;

        #choose specific cell
        action = actionData[0][0]
        cell = self.cells[cellIndex]

        #present on board
        if action == '1': # white
            cell.background_color = (1, 1, 1, 1)
        if action == '0': # black
            cell.background_color = (0, 0, 0, 1)


        #continue to next cells
        actionData[0] = actionData[0][1:]
        Clock.schedule_once(lambda a: self.performSolutionAction(actionData, cellIndex + 1), 0.1)



    # ---------------------------------------------- PART OF - UTILITIES
    # gets: list of widgets
    # returns:-
    # action: add widgets to view
    def addElements(self, dataList):
        for element in dataList:
            self.add_widget(element)

