
from kivy.uix.label import Label
from kivy.uix.button import Button
import cPickle as pickle


#incharge of solving current board
class GriddlerSolver:

    # gets:-
    # returns:-
    # action:init data
    def __init__(self,rowTitle,colTitle,cells,cols,rows):
        #data
        self.colTitle= rowTitle
        self.rowTitle = colTitle
        self.cells = cells

        #size
        self.cols = cols
        self.rows = rows

        print "cols : " , self.cols , " rows : ", self.rows

        #colors
        self.black = "1"
        self.yellow = "0"


    #-----------------------------------------CREATE ALL OPTIONS ALGORITHEM

    # --------- CREATES ALL OPTIONS GENERAL

    # gets: currentOption=> base option, allOptions=>all options so far, numSets=> num of black blocks, numWhites=> num of whites that can be
    # returns:-
    # action: create all options based on its limitations
    def createAllOptions(self, currentOption, allOptions, numSets, numWhites):

        #currentOption = list of indexes where the black blocks start = (I1(first black block index),I2(second black block index),....,InumSets)
        #if assigned an index for every block add it to the options
        if len(currentOption) == numSets:
            allOptions.append(currentOption)
            return

        #CREATE ALL COMBINATIONS

        #assign first index, if allready assigned we can start only after it
        firstIndex = 0
        if len(currentOption) > 0:
            firstIndex = currentOption[-1] + 1

        #add all options for begginings to this black blocks
        #it can be added only in range of --------------------- firstIndex : numWhites + 2 - <TOTAL NUM SETS> + <NUMBLOCKS ASSIGNED ALLREADY>
        #so the sets after it will be able to be added
        for i in xrange(firstIndex, numWhites + 2 - numSets + len(currentOption)):
            newOption = currentOption[:]
            newOption.append(i)

            #call recursivly for next black block
            self.createAllOptions(newOption, allOptions, numSets, numWhites);


    # gets: allNumbers => array of titles, totalLength => self.cols if calculating rows, self.rows if calc cols.
    # returns: all binary strings that represent all options for limitations of allNumbers in total size of totalLength
    # action: -
    def returnOptionsForGeneral(self,allNumbers,totalLength):
        try:
            # create base option
            base_options = ""
            for num in allNumbers:
                for i in xrange(int(num)):
                    base_options += self.black

                base_options += self.yellow

            base_options = base_options[:-1]


            # get number of sets of 1 -> hows many blocks of black there are
            numSets = len(base_options.split("0"))

            # sum all the limitiations of col
            sum = 0
            for num in allNumbers:
                sum += int(num)
            # save how many whites there are = self.rows - {num of limitations = num of blacks}
            numWhites = totalLength - sum

            # create all options based on base option
            allOptions = list()
            self.createAllOptions(list(), allOptions, numSets, numWhites);

            # if only one option
            if not isinstance(allOptions, list):
                allOptions = [allOptions]

            # return options as binary strings
            allBinaryStrings = self.returnBinaryForGeneral(allOptions,allNumbers,totalLength)
            return allBinaryStrings
        except:
            return list()


    # gets: options=> all options in format (I1(first black block index),I2(second black block index),....,InumSets), allNumbers => array of titles, totalLength => self.cols if calculating rows, self.rows if calc cols.
    # returns: options in binary
    # action:-
    def returnBinaryForGeneral(self, options,allNumbers,totalLength):

        # CREATE ALL OPTIONS
        binaryOptions = list()

        # sum the titles/limitations of current col
        sum = 0
        for num in allNumbers:
            sum += int(num)

        # create options
        for option in options:
            # add base zeros
            binaryString = "0" * (totalLength - sum)
            counter = 0

            # add ones according to indexs
            for currentIndex in option[::-1]:
                binaryString = binaryString[:currentIndex] + "1" * int(allNumbers[::-1][counter]) + binaryString[
                                                                                                    currentIndex:]
                counter += 1

            # add current options
            binaryOptions.append(binaryString)

        # return all options
        return binaryOptions



    #--------- ALL OPTIONS OF COLS

    # gets: current col to calculate its possible options
    # returns: returns all the options for this col in binary
    # action: create all options for this col based on its limitations
    def returnOptionsForCol(self, col):
        #get current col limitiations
        title = self.colTitle[col].text
        allNumbers = title.split("\n")

        return self.returnOptionsForGeneral(allNumbers,self.rows)


    # --------- ALL OPTIONS OF ROWS

    # gets: current row to calculate its possible options
    # returns: returns all the options for this row in binary
    # action: create all options for this row based on its limitations
    def returnOptionsForRow(self,row):
        title = self.rowTitle[row].text
        allNumbers =  title.split(" ")

        return self.returnOptionsForGeneral(allNumbers ,self.cols)


    # -----------------------------------------REDUCE ALGORITHEM

    # gets: -
    # returns: all possible options for cols
    # action: -
    def getRowsTableOptions(self):
        allPossibleCols = list()

        #run on all cols
        for col in xrange(self.cols):
            currentOptions = self.returnOptionsForCol(col)
            allPossibleCols.append(currentOptions)

        return allPossibleCols

    # gets: allOptions for rows
    # returns: all possible options for rows
    # action: reduces the  number of total options with the limitations on the rows
    def reduce(self, allOptions):
        #gets all the options of the rows
        allRowsOptions = self.getRowsTableOptions()
        reduceBy = 10000

        # reduce options
        for row in xrange(self.rows):
            # run on all row options
            currentOptions = allOptions[row]
            for currentRowOption in currentOptions:

                # run on all cols
                currentIndex = 0
                for currentCol in currentRowOption:
                    doesAccordinate = False
                    posRows = allRowsOptions[currentIndex]

                    if len(posRows) > reduceBy:
                        currentIndex += 1
                        continue

                    #check if possible
                    for currentEliminate in posRows:
                        if currentEliminate[row] == currentRowOption[currentIndex]:
                            doesAccordinate = True
                            break

                    #if no option was found that accordinates, remove option
                    if doesAccordinate == False:
                        allOptions[row].remove(currentRowOption)
                        break;

                    currentIndex += 1

        return allOptions


    # -----------------------------------------SOLVING ALGORITHEM

    # gets: table=> two dimension table that represents the current board
    # returns: true=> if board is valid with limitations of rows, false else
    # action: checks if board is valid with the limitations
    def isTableValid(self,table):
        #run on all cols
        for col in xrange(self.cols):
            #get col limitations
            numbers = self.colTitle[col].text.split("\n")
            originNumbers = self.colTitle[col].text.split("\n")

            #check if meets all limitations
            currentNumber = 0
            for row in xrange(len(table)):

                #if current cell is black
                if table[row][col] == self.black:
                    if currentNumber < len(numbers) and numbers[currentNumber] != 0: #if we are in a streak of blacks
                        numbers[currentNumber] = int(numbers[currentNumber]) - 1
                    else: #if found black with no streak
                        return False

                #if current cell is yellow
                if table[row][col] == self.yellow:
                    #if current yellow meets basic standarts
                    if ((row-1 >= 0 and table[row-1][col] != self.yellow) or (row == 0)) and not (currentNumber ==0 and numbers[currentNumber] ==  originNumbers[currentNumber]):
                        #if in streak of black and then a yellow show up
                        if numbers[currentNumber] != 0:
                            return False
                        else: #continue the streak of yellows
                            currentNumber +=1

        #return true if met all limitations
        return True


    # gets: -
    # returns: list that represent the solution of board or false if non found
    # action: solves board
    def solveGriddler(self):
        allPossibleRows = list()


        sum = 0
        print "before reduce:"
        for row in xrange(self.rows):
            currentOptions = self.returnOptionsForRow(row)
            allPossibleRows.append(currentOptions)

            print row, "length: ", len(allPossibleRows[row])
            sum += len(allPossibleRows[row])


        #reduce options
        for row in xrange(self.rows):
            currentOptions = self.returnOptionsForRow(row)
            allPossibleRows.append(currentOptions)

        self.reduce(allPossibleRows)
        #end reduce options


        print "after reduce : "
        for row in xrange(self.rows):
            print row, "length: ", len(allPossibleRows[row])
            sum -= len(allPossibleRows[row])

        print "reduced by:", sum

        print "got all data"
        print "get all options"



        # run on all options
        firstRow = allPossibleRows[0][0]
        allPossibleRows[0].pop(0)

        result = self.solveSpecificGriddler([firstRow], allPossibleRows[1:])

        # if found result return it
        if result != False:
            return result

        #run on all first row options
        while not len(allPossibleRows[0]) == 0:
            firstRow = allPossibleRows[0][0]
            allPossibleRows[0].pop(0)
            result = self.solveSpecificGriddler([firstRow], allPossibleRows[1:])

            #if found result return it
            if result != False:
                return result

        #if no option was found return false
        return False


    # gets: table=> current table that was made for board, nextAllRows=> all next options to add to table
    # returns: list that represent the solution of board or false if non found
    # action: solves board
    def solveSpecificGriddler(self,table,nextAllRows):
        #check if current table is valid
        if not self.isTableValid(table):
            return False

        #if table length is the size of the origin board we should end
        if len(table) == self.rows:
            return table

        #get the next solution for the next row first option
        currentAllPossibleRows = pickle.loads(pickle.dumps(nextAllRows, -1))
        firstRow = currentAllPossibleRows[0][0]
        currentAllPossibleRows[0].pop(0)

        #try solving with the new row
        currentTable = pickle.loads(pickle.dumps(table, -1))
        currentTable.append(firstRow)

        result = self.solveSpecificGriddler(currentTable, currentAllPossibleRows[1:])

        # if found result return it
        if result != False:
            return result

        #run on all other options of row
        while result == False and not len(currentAllPossibleRows[0]) == 0:
            firstRow = currentAllPossibleRows[0][0]
            currentAllPossibleRows[0].pop(0)

            #try solving with new row
            currentTable = pickle.loads(pickle.dumps(table, -1))
            currentTable.append(firstRow)
            result = self.solveSpecificGriddler(currentTable, currentAllPossibleRows[1:])

            # if found result return it
            if result != False:
                return result

        #if no option was found return false
        return False

