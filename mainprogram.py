'''
It imports the snakegame classes into the main program to run 
This block creates an instance of SnakeGame and starts the game when the script is executed.
'''
from snakegame import *

# Main function to start the game
if __name__ == "__main__":    #This condition ensures that the code block inside it only runs when the script
    #is executed directly, and not when it is imported
    
    game = SnakeGame()  # Create a SnakeGame instance
    #This line creates an instance of the SnakeGame class and assigns it to the variable game.
    
    game.play()  # Start the game
    #This line starts the game by calling the play method on the game object, 
    #which is an instance of the SnakeGame class.
