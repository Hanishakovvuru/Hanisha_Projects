# Memory game by Hanisha Kovvuru
# The player tries to find two matching tiles by selecting tiles from a rectangular grid.
# A single-person game that tracks the score of the player as the time taken to complete the game, where a lower score is better.
# Multiple players can take turns playing the game and compete by comparing their scores.

import pygame
import random
import time

# User-defined functions

def main():
    # Initialize pygame
    pygame.init()
    # create a pygame display window and get its surface
    w_surface = pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Memory')   
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game
        self.surface = surface
        self.black = 'black'
        self.bg_color = pygame.Color(self.black)
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
        
        # === game specific objects
        self.thousand = 1000
        self.board_size = 4
        self.board = []
        self.score = 0
        self.selected_tile = []
        self.create_board()

    def create_board(self):
        # Create the game board.
        # - self is the Game whose board is created       
        
        # Width of each tile is the total surface width divided by 5 (need a 5th row to display the score on a black surface) and height is just 4 parts of the surface height
        # They are 5 rows and 4 columns
        
        width = self.surface.get_width() // (self.board_size + 1)
        height = self.surface.get_height() // self.board_size
        index = 0
        # All images that will be revealed as the player clicks on the tiles
        self.filenames = ['image1.bmp','image2.bmp','image3.bmp','image4.bmp','image5.bmp','image6.bmp','image7.bmp','image8.bmp']
        # The default (? mark) image which is assigned to all tiles to hide the real images
        self.default_filename = 'image0.bmp' 
        # We need all 8 images twice
        self.filenames = self.filenames + self.filenames
        random.shuffle(self.filenames)
        
        # for each row index
        for row_index in range(0,self.board_size):
         # create row as an empty list
            row = []
            # for each column index
            for col_index in range(0,self.board_size):
                # create tile using row index and column index
                x = col_index * width 
                y = row_index * height
                # Creates a tile object for every column in each row of the board
                tile = Tile(x,y,width, height, self.filenames[index], self.default_filename, self.black, self.surface)
                # append tile to row
                row.append(tile)
                # Increases the index by one, which allows to call for the next item in the self.filenames list when loop is run again
                index = index + 1
            # append row to board
            self.board.append(row)
        

    def play(self):
        
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
        
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
                self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second 

    def handle_event(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            # Check if pygame is told to quit (window is closed)
            if event.type == pygame.QUIT:
                # Stops the game
                self.close_clicked = True
            # Check if the mouse button is released (after pressing)
            elif event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                # Call to the handle_mouse_up function that implements the actions to be taken after mouse button up event has happened
                self.handle_mouse_up(event)
                
    
    def handle_mouse_up(self, event):
        # Respond to the player releasing the mouse button by
        # taking appropriate actions.
        # - self is the Game where the mouse up occurred.
        # - event is the pygame.event.Event object to handle
        
        # for each row
        for row in self.board:
            # for each column or tile in the row
            for tile in row:
                # The three if conditions check for whether the tile is clicked, the tile is not exposed and they are maximum of two tile filenames under self.selected_tile respectively. 
                if tile.get_rect().collidepoint(event.pos) and not tile.get_expose() and len(self.selected_tile) <= 2:
                    # Collect the selcted tiles under a empty list (self.selected_tile)
                    self.selected_tile.append(tile)
                    # Expose the tile by calling the tile class (to create a tile object) and setting self.expose to be true
                    tile.set_expose(True)
        
    def draw(self):
        # Draw all game objects
        # - self is the Game to draw 
        
        self.surface.fill(self.bg_color) # clear the display surface first
        # Display the score
        self.show_score(self.score)
        
        # Draw each tile to the surface
        for row in self.board:
            for tile in row:
                # Call to the tile class and draw function (under tile class) allows for the tile to be drawn onto the surface
                tile.draw()
        
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        
        # Update the game objects.
        # - self is the Game to update
        
        # Tracks the score by recording the seconds passed since the start of the game
        self.score = pygame.time.get_ticks()//self.thousand
        
        # When two tiles are selected 
        if len(self.selected_tile) == 2:         
            # If the filename of the first tile and the the filename of the second tile are the same
            if self.selected_tile[0].get_filename() == self.selected_tile[1].get_filename() :
                # We reduce the speed of the game to expose the selected tiles for short time
                pygame.time.delay(self.thousand)
                
                # For the two tiles selected
                for i in range(2):
                    # Set the tile to stay exposed
                    self.selected_tile[i].set_expose(True)
                    # Draw the exposed tile image permanently
                    self.selected_tile[i].draw()
                # Remove all the tiles under the self.selected_tile list. This needs to be done so we can look at the next two selected tiles. Two tiles are compared at once.
                self.selected_tile.clear()
            
            # If the filename of the first tile is not same as the filename of the second tile
            elif self.selected_tile[0].get_filename() != self.selected_tile[1].get_filename():
                # We reduce the speed of the game to expose the selected tiles for short time
                pygame.time.delay(self.thousand)
                
                # For the two tiles selected
                for i in range(2):
                    # Set the tile to not stay exposed
                    self.selected_tile[i].set_expose(False)
                    # Draw the default tile image
                    self.selected_tile[i].draw()
                # Remove all the tiles under the self.selected_tile list. This needs to be done so we can look at the next two selected tiles. Two tiles are compared at once.
                self.selected_tile.clear()
                
    def show_score(self, score):
        # Makes the score (time passed in second) of the player appear on the screen in the top right corner
        # - score is the int seconds passed since the start of the game
        
        # Show the game score in white 72 font size at the top right corner
        text_string = str(score)
        fontsize = 72
        fg_color = 'white'
        text_font = pygame.font.SysFont('', fontsize)
        text_image = text_font.render(text_string, True, fg_color, self.bg_color)
        location = (self.surface.get_width()-text_image.get_width(),0)
        self.surface.blit(text_image, location)

    def decide_continue(self):
        # Determine if the game should continue
        # - self is the Game to update
        
        # Integer variable to keep track of how many tiles are exposed on the board
        num_exposed_tile = 0
        
        # For every row in the board
        for row in self.board:
            # for every column/tile in the row
            for tile in row:
                # If the tile is exposed
                if tile.get_expose():
                    # Increase the integer variable by 1
                    num_exposed_tile +=1
        
        # If all 16 tiles are exposed
        if num_exposed_tile == 16:
            # The game ends
            self.continue_game = False 

class Tile:
    # An object in this class represents a Rectangular tile
    # that contains two images (default and hidden image).
    # A tile can be selected if the tile is not exposed yet.
    # If the non-exposed tile is selected its hidden image is exposed.

    def __init__(self, x, y, width, height, filename, default_filename, fg_color, surface):
        # Initialize a tile to contain an image
        # - x is the int x coord of the upper left corner
        # - y is the int y coord of the upper left corner
        # - width is the int width of the tile
        # - height is the int height of the tile
        # - filename is the list of filenames of all the hidden images
        # - default_filename is the string filename of the default image
        # - fg_color is the string foreground colour of the rectangle underneath the image of the tile
        
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.surface = surface
        self.fg_color = pygame.Color(fg_color)
        self.border_width = 3
        self.filename = filename
        self.default_filename = default_filename
        # A boolean varaible which signifies whether a tile is exposed or not. It's initial value is set to false since the game starts with no tiles being exposed.
        self.expose = False
       
    def draw(self):
        # Draw the Tile's image and a rectangle black border
        # - self is the Tile
        
        # If the tile is set to expose
        if self.expose:
            # Draw the hidden image of the tile onto the tile's surface
            self.surface.blit(pygame.image.load(self.filename),(self.x, self.y))
        
        # If the tile is not set to expose
        else:
            # Draw the default image of the tile onto the tile's surface
            self.surface.blit(pygame.image.load(self.default_filename),(self.x, self.y))
            
        # Draw the black rectangle border of all tiles
        pygame.draw.rect(self.surface, self.fg_color, self.rect, self.border_width)
    
    def get_expose(self):
        # A getter method that gets whether a tile is exposed (True) or not exposed (False)
        return self.expose
    
    def set_expose(self, expose):
        # A setter method that sets the self.expose to any boolean expression we want
        # - expose is the boolean value that is used to set to the self.expose variable
        self.expose = expose
    
    def get_rect(self):
        # A getter method that gets the surface of the rectangle of a tile
        return self.rect
    
    def get_filename(self):
        # A getter method that gets the hidden filename of a tile
        return self.filename


main()
