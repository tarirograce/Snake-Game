'''
This is a simple, text-based Snake game designed to run in the terminal. 
In this game, the player controls a snake using the "W", "A", "S", and "D" keys to 
move up, left, down, and right, respectively.The goal is to guide the snake to eat food, 
represented by the character "@". Each time the snake eats food, it grows longer.
The snake's body is represented by "S" characters. The game ends if the snake hits 
the wall or its own body.Food appears in random positions on the screen each time it's eaten,
making each game unique.
*-----------------*
Game Setup: Constants define screen size, snake, and food characters. Directions are mapped as constants 
for easy input processing.

SnakeGame Class: Handles initializing the game, generating food, updating the snake's position, 
checking collisions, and handling user inputs.

Main Game Loop: Continuously updates the game state based on user input until the game ends.
'''
import random
'''
The random module is imported to allow random placement of food on the screen. This module's 
functions are used to randomly generate the x and y coordinates for the food each time it appears.
'''

# Game constants
BWIDTH = 30  # Width of the game screen
BHEIGHT = 15  # Height of the game screen
S_CHAR = "S"  # Character representing the snake's body
FOOD_CHAR = "@"  # Character representing the food
EMPTY = "-"  # Character representing empty spaces on the screen

'''
These constants define the game board's appearance:
• BWIDTH and BHEIGHT set the width and height of the screen.
• S_CHAR is the character used to represent the snake's body.
• FOOD_CHAR represents the food.
• EMPTY represents empty spaces on the screen.
'''

# Directions for snake movement and name the variables as it supposed to work 
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
'''
These constants represent the four possible directions the snake can move in. 
They help make direction-related code easier to understand and less error-prone.
'''

# Global variable for highest score
highest_score = 0  # This variable keeps track of the highest score across games.

# Snake game class
class SnakeGame:
    def __init__(self):
        '''
        Initializes the game state and variables:
        - snake starts at the center of the board.
        - no food initially placed.
        - direction is set to RIGHT.
        - score is initialized to 0.
        - game over flag is set to False.
        '''
        self.snake = [(BHEIGHT // 2, BWIDTH // 2)]  # Start the snake at the center of the screen
        self.food = None  # No food at the beginning
        self.direction = RIGHT  # Initial direction is to the right
        self.score = 0  # Initial score is 0
        self.game_over = False  # Game is active until the snake hits a wall or itself
        self.CreateFood()  # Generate the first food item
        self.load_highest_score()  # Load the highest score from the file when the game starts

    def CreateFood(self):
        '''
        Place food at a random location on the screen, ensuring it does not overlap with the snake's body.
        '''
        FoodX = random.randint(0, BHEIGHT - 1)  # Randomly choose x-coordinate for food
        FoodY = random.randint(0, BWIDTH - 1)   # Randomly choose y-coordinate for food
        
        # Ensure food does not appear on the snake's body
        while (FoodX, FoodY) in self.snake:
            FoodX = random.randint(0, BHEIGHT - 1)
            FoodY = random.randint(0, BWIDTH - 1)

        self.food = (FoodX, FoodY)  # Set food position to chosen coordinates

    def move(self):
        '''
        Moves the snake in the current direction and handles collisions with food, walls, and itself.
        '''
        HeadX, HeadY = self.snake[0]  # Get the current head position of the snake
        
        # Update the head position based on the current direction
        if self.direction == UP:
            HeadX -= 1  # the snake's head moves up by decreasing HeadX.
        elif self.direction == DOWN:
            HeadX += 1  # the snake's head moves down by increasing HeadX.
        elif self.direction == LEFT:
            HeadY -= 1  # the snake's head moves left by decreasing HeadY.
        elif self.direction == RIGHT:
            HeadY += 1  # the snake's head moves right by increasing HeadY.
        
        NewHead = (HeadX, HeadY)  # New position of the snake's head
        self.snake.insert(0, NewHead)  # Add new head position to the front of the snake's body

        # Check if the snake eats the food
        if NewHead == self.food:  # If the new head position is the same as the food's
            self.score += 1  # Increase score
            self.CreateFood()  # Generate new food at a random position
        else:
            self.snake.pop()  # Remove tail if the snake didn't eat food (snake only grows if it eats food)

        # Check for collisions with walls or itself
        if not (0 <= HeadX < BHEIGHT and 0 <= HeadY < BWIDTH) or NewHead in self.snake[1:]:
            self.game_over = True  # Set game over if the snake hits the wall or itself

    def change_direction(self, new_direction): 
        '''
        Changes the snake's direction, ensuring it does not reverse directly into itself.
        '''
        if self.direction == UP and new_direction != DOWN:
            self.direction = new_direction
        elif self.direction == DOWN and new_direction != UP:
            self.direction = new_direction
        elif self.direction == LEFT and new_direction != RIGHT:
            self.direction = new_direction
        elif self.direction == RIGHT and new_direction != LEFT:
            self.direction = new_direction

    def DrawBorder(self):
        '''
        Provides the game screen, including the snake, food, and the game board's border. 
        Displays the player's current score.
        '''
        print("^" + "-" * BWIDTH + "^")  # Top border
        for row in range(BHEIGHT):        
            line = "|"
            for col in range(BWIDTH): 
                if (row, col) in self.snake:
                    line += S_CHAR  # Display snake character
                elif (row, col) == self.food:
                    line += FOOD_CHAR  # Display food character
                else:
                    line += EMPTY  # Display empty character
            line += "|"
            print(line)
        print("^" + "-" * BWIDTH + "^")  # Bottom border
        print("Score: {}".format(self.score))  # Display the score

    def load_highest_score(self):
        '''
        Loads the highest score from a file ("scores.txt"). If the file doesn't exist or contains invalid data,
        initializes the highest score to zero.
        '''
        global highest_score
        try:
            with open("scores.txt", "r") as file:
                highest_score = int(file.read().strip())  # Read the highest score from the file
        except FileNotFoundError:
            print("No score file found. Starting with score 0.")  # Inform user if file is missing
        except ValueError:
            print("Invalid data in score file. Starting with score 0.")  # Handle corrupted data in file

    def save_highest_score(self):
        '''
        Saves the current highest score to a file ("scores.txt") for persistence across game sessions.
        '''
        global highest_score
        try:
            with open("scores.txt", "w") as file:
                file.write(str(highest_score))  # Write the highest score to the file
        except Exception as e:
            print(f"Error saving score: {e}")  # Error handling for file operations

    def play(self): 
        '''
        Starts the main game loop, which continues until the game ends due to collision or the player quitting.
        '''
        global highest_score
        self.score = 0  # Reset score for each new game

        while not self.game_over:
            self.DrawBorder()  # Display the game board

            # Get user input for movement direction
            move = input("Enter your move (W for 'UP', A for 'LEFT', S for 'DOWN', D for 'RIGHT', Q to Quit): ").strip().upper()

            # Validate the move input
            if move == "W":
                self.change_direction(UP)
            elif move == "A":
                self.change_direction(LEFT)
            elif move == "S":
                self.change_direction(DOWN)
            elif move == "D":
                self.change_direction(RIGHT)
            elif move == "Q":
                print("Exiting the game. Goodbye!")
                break
            else:
                print("Invalid move. Please use W, A, S, or D only.")
                continue  # Skip the rest of the loop and wait for valid input

            # Move the snake in the current direction
            self.move()

        # Update highest score if the current score is higher
        if self.score > highest_score:
            highest_score = self.score

        # Save the highest score to a file after the game ends
        self.save_highest_score()

        # Display game over message and final score
        print("\nGame Over! Thank you for playing")
        print("Congratulations! Your final score is: {}".format(self.score))
        print(f"Highest Score: {highest_score}")  # Display the highest score.

        # Ask player if they want to play again
        play_again = input("Do you want to play again? (Y/N): ").strip().upper()
        if play_again == "Y":
            self.game_over = False  # Reset game over status for new game
            self.snake = [(BHEIGHT // 2, BWIDTH // 2)]  # Reset snake position
            self.food = None  # Reset food
            self.direction = RIGHT  # Reset direction
            self.score = 0  # Reset score
            self.CreateFood()  # Generate new food for the next game
            self.play()  # Start a new game
        else:
            print("Thanks for playing!")  # Thank the player and end the program
            return

