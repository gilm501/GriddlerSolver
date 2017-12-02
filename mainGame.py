from kivy.app import App
from kivy.core.window import Window

from algorithems.cloneGame import CloneGame
from gameBoard import GameBoard


#main program
#creates game view
class mainGame(App):
    def build(self):
        #init game view
        self.appData = GameBoard()
        return self.appData;



#start game
if __name__ == "__main__":
    #Window.fullscreen = True
    app = mainGame()
    app.run()

