# Pong game - a two player game by Hanisha Kovvuru
# press q key to move the left white rectangle towards the top edge of the window
# press a key to move the left white rectangle towards the bottom edge of the window
# press p key to move the right white rectangle towards the top edge of the window
# press l key to move the right white rectangle towards the bottom edge of the window
# The left player gets points when they manage to make the ball hit the right edge of the window 
# The right player gets points when they manage to make the ball hit the left edge of the window
# Whoever first reaches 11 points wins!

# Credits: Used pong-hints.py as a foundation to start my code. Also, used certain segemnts of code from pre-poke framework (.py) and Poke the Dots v3 (.py) in my code.

import pygame, random, math

# User-defined functions
def main():
    # initialize all pygame modules 
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Pong')
    # get the display surface
    w_surface = pygame.display.get_surface() 
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
        self.bg_color = 'black'
        self.fg_color = 'white'
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
               
        # === game specific objects
        # Paddle
        self.paddle_increment = 15
        self.left_paddle_x_coord = 125
        self.right_paddle_x_coord  = 375
        paddle_width = 10
        paddle_height = 50
        self.left_paddle = Paddle(self.left_paddle_x_coord,self.surface.get_height()//2,paddle_width,paddle_height,self.fg_color,self.surface)
        self.right_paddle = Paddle(self.right_paddle_x_coord,self.surface.get_height()//2,paddle_width,paddle_height,self.fg_color,self.surface)   
        
        # Ball
        self.small_ball_radius = 5
        self.four = 4  # Need to use this literal multiple times, so assigned it to a variable
        self.small_ball_x_coord = random.randint(self.left_paddle_x_coord, self.right_paddle_x_coord)  # The ball should start near the horizontal-center of the window (between the left and right paddles), to start the game fairly
        self.small_ball_y_coord = random.randint(self.small_ball_radius, self.surface.get_height() - self.small_ball_radius)
        self.small_ball_center = [self.small_ball_x_coord, self.small_ball_y_coord]
        self.small_ball_velocity = [self.four,1]
        self.small_ball = Ball(self.fg_color,self.small_ball_radius, self.small_ball_center, self.small_ball_velocity, self.surface)
        
        # Initialize scores of the two players
        self.left_score = 0
        self.right_score = 0


    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            # Checks if the pygame window is closed
            if event.type == pygame.QUIT:
                self.close_clicked = True
            # Checks if any key on the keyboard is pressed
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            # Checks if any key on the keyboard is released
            elif event.type == pygame.KEYUP:
                self.handle_key_up(event)


    def handle_key_down(self,event):
        # reponds to KEYDOWN event (when key is pressed)
        # - self is the Game object
        
        if event.key == pygame.K_a:
            # Moves left paddle up when a is pressed
            self.left_paddle.set_vertical_velocity(self.paddle_increment)
        elif event.key == pygame.K_q:
            # Moves the left paddle down when q is pressed
            self.left_paddle.set_vertical_velocity(-self.paddle_increment)
        if event.key == pygame.K_l:
            # Moves the right paddle up when l is pressed
            self.right_paddle.set_vertical_velocity(self.paddle_increment)
        elif event.key == pygame.K_p:
            # Moves the right paddle down when p is pressed
            self.right_paddle.set_vertical_velocity(-self.paddle_increment)        

    def handle_key_up(self,event):
        # responds to KEYUP event (when key is released)
        # - self is the Game object
        
        if event.key == pygame.K_a:
            # Makes the left paddle stationary when a is released 
            self.left_paddle.set_vertical_velocity(0)
        elif event.key == pygame.K_q:
            # Makes the left paddle stationary when q is released
            self.left_paddle.set_vertical_velocity(0)
        if event.key == pygame.K_l:
            # Makes the right paddle stationary when l is released
            self.right_paddle.set_vertical_velocity(0)
        elif event.key == pygame.K_p:
            # Makes the right paddle stationary when p is released 
            self.right_paddle.set_vertical_velocity(0)         

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(pygame.Color(self.bg_color)) # clear the display surface first
        self.show_score()
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.small_ball.draw()
      
        pygame.display.update() # make the updated surface appear on the display


    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        
              
        self.left_paddle.move()
        self.right_paddle.move()
        self.small_ball.move()
        self.collide()
        self.score()
        
    def collide(self):
        # Checks if the ball collides with the paddles on the relative side and make the ball bounce. 
        
        # Makes the ball only bounce off right side of the left paddle
        if self.left_paddle.rect.collidepoint(self.small_ball_center) and self.small_ball_velocity[0] == -self.four:
            for i in range(0,2):
                self.small_ball_velocity[i] = - self.small_ball_velocity[i]

        # Makes the ball only bounce off left side of the right paddle
        if self.right_paddle.rect.collidepoint(self.small_ball_center) and self.small_ball_velocity[0] == self.four:
            for i in range(0,2):
                self.small_ball_velocity[i] = - self.small_ball_velocity[i]
        
            
    def score(self):
        # Tracks the socre of the left and right players 
        
        if self.small_ball_center[0] >= self.surface.get_width() - self.small_ball_radius:
            self.left_score += 1        
        if self.small_ball_center[0] <= self.small_ball_radius:
            self.right_score += 1
       
        
    def show_score(self):
        # Makes the score of the left and right player appear on the screen in their relative places
        
        # Applies to both left and right score images
        fontsize = 72
        text_font = pygame.font.SysFont('', fontsize)
        
        # Specific to left score image 
        left_text_string = str(self.left_score)
        left_text_image = text_font.render(left_text_string, True, self.fg_color, self.bg_color)
        left_location = (0,0)   
        
        # Specific to right score image
        right_text_string = str(self.right_score)
        right_text_image = text_font.render(right_text_string, True, self.fg_color, self.bg_color)
        right_location = (self.surface.get_width()-right_text_image.get_width(),0)
        
        # Draw the score of the left and right player
        self.surface.blit(left_text_image, left_location)  
        self.surface.blit(right_text_image, right_location)

    def decide_continue(self):
        # Check and remember if the game should continue
        # Stops the game when score reaches 11
        # - self is the Game to check
        eleven = 11
        if self.left_score >= eleven or self.right_score >= eleven:
            self.continue_game = False

class Paddle:
    # An object in this class represents a Paddle that moves

    def __init__(self,x,y,width,height,color,surface):
        # - self is the Paddle object
        # - x, y are the top left corner coordinates of the rectangle of type int
        # - width is the width of the rectangle of type int
        # - height is the height of the rectangle of type int
        # - surface is the pygame.Surface object on which the rectangle is drawn

        self.rect = pygame.Rect(x,y,width,height)
        self.color = pygame.Color(color)
        self.surface = surface
        self.vertical_velocity = 0  # paddle is not moving at the start
    def draw(self):
        # - self is the Paddle object to draw
        pygame.draw.rect(self.surface,self.color,self.rect)
    def set_vertical_velocity(self,vertical_distance):
        # set the vertical velocity of the Paddle object
        # - self is the Paddle object
        # - vertical_distance is the int increment by which the paddle moves vertically
        self.vertical_velocity = vertical_distance
    def move(self):
        # moves the paddle such that paddle does not move outside the window
        # - self is the Paddle object
        
        # Allows the movement of the rectangle
        self.rect.move_ip(0, self.vertical_velocity) 
        # Stops the paddle from going above the top of the window
        if self.rect.bottom >= self.surface.get_height():
            self.rect.bottom = self.surface.get_height()
        # Stops the paddle from going below the bottom of the window
        elif self.rect.top  <= 0:
            self.rect.top = 0
            
class Ball:
    # An object in this class represents a Ball that moves
    
    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
        # - self is the Ball object 
        # - ball_color is the color of the ball
        # - ball_center is the x and y coordinates of the ball of type list
        # - ball_velocity is the velocity of the ball in x and y direction of type list
        # - surface is the pygame.Surface object on which the ball is drawn
        
        
        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface
    
    def move(self):
        # - moves the ball that is stays within the game window
        # - self is the Ball object
        
        size = self.surface.get_size() # (500, 400)
        
        # Moves the ball in both x and y direction
        for i in range(0,2):
            self.center[i] = self.center[i] + self.velocity[i]
        
        # Makes the ball be inside the window
        for i in range(0,2):
            if self.center[i] < self.radius:
                # reached the minimum for this coordinate (left and top), bounce back
                self.velocity[i] = - self.velocity[i]
            if self.center [i] + self.radius > size[i]:
                # reached the maximum for this coordinate (right and bottom), bounce back
                self.velocity[i] = - self.velocity[i] 
                
    def draw(self):
        # - self is the Ball object to draw
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)
        
main()
