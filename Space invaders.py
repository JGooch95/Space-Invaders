#Imports all of the necessary modules
import pygame, time, sys, random
from pygame.locals import *
from timeit import default_timer

#Initiates pygame
pygame.init()

#Defines the game clock used to limit the games frame rate
Clock = pygame.time.Clock()

#Defines the colours used for objects
BLACK = [0,0,0]
WHITE = [255,255,255]
GREEN = [0, 255, 0]
RED = [255, 0, 0]

class Screen:
    #Defines the size variables for the window
    WIDTH = 800
    HEIGHT = 600
    
    def Setup(self):
        #Draws the window with a caption.
        self.Window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pygame.display.set_caption("Space Invaders")

        #Sets the game icon
        self.Icon = pygame.image.load("Game Images/SI_Icon.jpg")
        pygame.display.set_icon(self.Icon)

        #Makes the mouse invisible.
        pygame.mouse.set_visible(False)
        
    def Refresh(self):
        #Refreshes the images on the screen limiting it to 60 times per second.
        pygame.display.update()
        Clock.tick(60)
        
class Background:
    #Declares the movement per iteration in the x axis for the background.
    MoveX = 1
    Moving = True
    
    def Animate(self):
        #Animates the background by having 2 images which move across the screen side by side
        #When one leaves the right side of the screen its X position changes to the left side
        
        #Increases the x value of the X of both of the images which are moving across the screen
        #by however many pixels it moves per iteration
        if self.Moving == True:
            self.BG_1.X += self.MoveX
            self.BG_2.X += self.MoveX

        #Draws the images to the screen with the new positions and writes the toggle text to the screen.
        Screen.Window.blit(self.BG_1.Image, (self.BG_1.X ,self.BG_1().Y))
        Screen.Window.blit(self.BG_2.Image, (self.BG_2.X ,self.BG_2().Y))
        
        #Changes the X position of the image to the left side of the screen
        #if the image leaves the right side of the screen.
        if self.BG_1.X >= Screen.WIDTH or self.BG_1.X < -1600:
            self.BG_1.X = -1600
        if self.BG_2.X >= Screen.WIDTH or self.BG_2.X < -1600:
            self.BG_2.X = -1600
            
    def Write_Prompt(self):
        Text = ('Press Z to Pause the background')
        Font = pygame.font.SysFont('Agency FB', 18)
        Write_line(Text, Font, WHITE, 700, 580, "Center")
        
    def Toggle(self):
        if self.Moving == True:
            self.Moving = False
            
        elif self.Moving == False:
            self.Moving = True
        
    class BG_1:
        #Holds all of the image properties for the first background image
        #Position
        X = 0
        Y = 0
    
        #Image file
        File_name = "Game Images/Stars.jpg"
        Image = pygame.image.load(File_name)
        

    class BG_2:
        #Holda all of the image properties for the second background image
        #Position
        X = -1600
        Y = 0

        #Image file
        File_name = "Game Images/Stars.jpg"
        Image = pygame.image.load(File_name)
        
class Player:
    #Declares the location of the player sprite in the file
    Image = "Game Images/Sprites/Player.png"

    def Respawn(self):
        #Declares the player positional variables
        self.X = 100
        self.Y = 495

        #Declares the player movement variables
        self.MoveSpeed = 3
        self.MoveX = 0

        #Declares the players tank sprite
        self.Sprite = pygame.image.load(self.Image).convert_alpha()

        #Declares the players area variable.
        Player.Hitbox = [pygame.Rect((Player.X, Player.Y + 34),(94, 34)),pygame.Rect((Player.X + 34 , Player.Y),(94, 34))]
        
    def Controls(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #Allows the player to control the tank.
                #When ___ key is pressed Movement in x direction
                #is in right direction at the set movespeed.
                if event.key == K_RIGHT or event.key == K_d:
                    self.MoveX = Player.MoveSpeed

                #When ___ key is pressed Movement in x direction
                #is in left direction at the set movespeed.
                if event.key == K_LEFT or event.key == K_a:
                    self.MoveX = -Player.MoveSpeed
                    
                #When ___ key is pressed the game confirms the gun should shoot.    
                if (event.key == K_UP or event.key == K_SPACE or event.key == K_w) and Player.Bullet.Loaded == True:
                    Player.Bullet.Fire = True    

                #When escape is pressed the game pauses.    
                if event.key == K_ESCAPE:
                    Player.MoveX = 0
                    Player.Bullet.Fire = False
                    Game.Pause()
                    
                if event.key == K_z:
                    Background.Toggle()
       
            if event.type == KEYUP:
                #If the direction keys are let go the player stops moving
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_a or event.key == K_d:
                    self.MoveX = 0

                #If ___ is let go then the code states the gun should not shoot.
                if (event.key == K_UP or event.key == K_SPACE or event.key == K_w):
                    Player.Bullet.Fire = False

            #If the X in the top corner of the window is clicked the game shuts down.        
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                    
        #Changes the X coordinate by the movespeed and direction set.
        Player.X += self.MoveX
        Player.Hitbox = [pygame.Rect((Player.X, Player.Y + 34),(94, 34)),pygame.Rect((Player.X + 34 , Player.Y),(24, 68))]

        #States that if the player moves past the right side of the screen then the player stops moving.
        if Player.X > Screen.WIDTH - 94:
            Player.X = Screen.WIDTH - 94
        #States that if the player moves past the left side of the screen then the player stops moving.
        if Player.X < 0:
            Player.X = 0
        
    class Bullet:
        #Declares the display variables.
        Image = "Game Images/Sprites/Bullet.jpg"
        Sprite = pygame.image.load(Image)

        #Declares whether the bullet is able to be shot.
        Loaded = True

        #Storage location for the bullets being shot.
        List =[]

        #Declares the amount of seconds between when the can shoot and the next shot.
        Reload_Speed = 0.8

        #Declares whether the bullet has been stated to be shot.
        Fire = False
        
        def Reset():
            #Resets the players bullets
            Player.Bullet.Loaded = True
            Player.Bullet.Fire = False
            Player.Bullet.List = []
            Player.Bullet.Reload_Speed = 0.8
            Player.Bullet.Timer.Started = False
            
        class Timer:
        #Timer which times the period in which the power up has been running
            #Declares the time the timer started.
            Start_point = 0
            
            #States whether the timer is running
            Started = False

            def Start():
                #Starts the timer when called by making the start time equal to
                #the present time and declaring that the timer has started and the bullet is unloaded.
                Player.Bullet.Timer.Start_point = default_timer()
                Player.Bullet.Timer.Started = True
                Player.Bullet.Loaded = False

            def Check(Time):
                #Checks if the duration of time has passed the time in which the timer was timing
                #if it has then the timer stops and the bullet is loaded again.
                Duration = default_timer() - Player.Bullet.Timer.Start_point
                Font = pygame.font.SysFont('Agency FB', 30)
                if Duration > Time:
                     Player.Bullet.Timer.Started = False
                     Player.Bullet.Loaded = True

        def Shoot():
            #Shoots the bullet out of the tank
            #States that if the bullet is loaded then the hitbox is made and
            #the bullet is shot out of the tank.
            if Player.Bullet.Loaded == True:
                Hitbox = Player.Bullet.Sprite.get_rect()
                Hitbox.x = Player.X + 40
                Hitbox.y = Player.Y + 22
                Player.Bullet.List.append(Hitbox)
                Player.Bullet.Timer.Start()

        def Shooting():
            #Resumes the movement of the shots which have been shot and performs collision detection.
            #If the bullet is not loaded then the timer to check when another bullet can be shot.
            if Player.Bullet.Loaded == False:
                Player.Bullet.Timer.Check(Player.Bullet.Reload_Speed)

            #If the list of bullets is not empty then...
            if len(Player.Bullet.List) > 0:
                #Every bullet in the list moves down by 3 pixels and is the drawn to the screen.
                for item in Player.Bullet.List:
                    item.y -=3
                    Screen.Window.blit(Player.Bullet.Sprite, (item.x, item.y))

                    #If the bullet passes the bottom of the screen then the bullet is removed from the list
                    if item.y < -22:
                        Player.Bullet.List.remove(item)
                        Player.Bullet.Shooting()
                        break

                    #Checks each alien to check if they have been hit by a bullet. If they are hit by a bullet then
                    #The Score is increased by the alien score. The alien is then stated as destroyed and a chance is
                    #Given for a power up to drop.
                    for Box in range(len(Alien.MoveBox.Rects)):
                        if item.colliderect(Alien.MoveBox.Rects[Box]):
                            for alien in range(len(Alien.RowLists.Hitboxes[Box])):
                                if item.colliderect(Alien.RowLists.Hitboxes[Box][alien]):
                                    if Alien.RowLists.Statuses[Box][alien] == "Alive":
                                            HUD.Score += Alien.RowLists.Scores[Box][alien]
                                            Alien.RowLists.Statuses[Box][alien] = "Destroyed"
                                            Randomiser = random.randint(0,10)
                                            if Randomiser == 1:
                                                PowerUps.Drop(Alien.RowLists.Hitboxes[Box][alien].x,Alien.RowLists.Hitboxes[Box][alien].y)

                                            Player.Bullet.List.remove(item)
                                            Player.Bullet.Shooting()
                                            break
                  
class Alien:    
    class RowLists:
        def Reset():
            #Resets the lists which store alien data to empty lists.
            Alien.RowLists.Sprites =[]
            Alien.RowLists.Statuses =[]
            Alien.RowLists.Hitboxes =[]
            Alien.RowLists.Scores = []
        
    class Type1:
        #Declares the location of the sprite in the file
        Image = "Game Images/Sprites/Enemies/Alien 1.png"
        def init():
            #Finds the image from the location and loads it.
            Alien.Type1.Sprite = pygame.image.load(Alien.Type1.Image).convert_alpha()
            
    class Type2:
        #Declares the location of the sprite in the file
        Image = "Game Images/Sprites/Enemies/Alien 2.png"
        def init():
            #Finds the image from the location and loads it.
            Alien.Type2.Sprite = pygame.image.load(Alien.Type2.Image).convert_alpha()
            
    class Type3:
        #Declares the location of the sprite in the file
        Image = "Game Images/Sprites/Enemies/Alien 3.png"
        def init():
            #Finds the image from the location and loads it.
            Alien.Type3.Sprite = pygame.image.load(Alien.Type3.Image).convert_alpha()
            
    class Type4:
        #Declares the location of the sprite in the file
        Image = "Game Images/Sprites/Enemies/Alien 4.png"
        def init():
            #Finds the image from the location and loads it.
            Alien.Type4.Sprite = pygame.image.load(Alien.Type4.Image).convert_alpha()
            
    class MoveBox:
        def Reset():
            #States the area variables for the movement boxes.
            Alien.MoveBox.Width = 700
            Alien.MoveBox.Height = 76

            #States the direction for the movement boxes.
            Alien.MoveBox.Direction = "Left"

            #States the positional variables for the movement boxes.
            Alien.MoveBox.X = 0
            Alien.MoveBox.Ypositions = []

            #States whether the boxes should be shown on the screen.
            Alien.MoveBox.Toggle = False

            #Stores the moveboxes for each row.
            Alien.MoveBox.Rects = []
        
        def Move():
            #States that the movement speed is dependant on the level the player is on.
            Alien.MoveBox.MoveSpeed = 1 + (HUD.Level * 0.2)

            #The rows which need to be drawn's coordinates are calculated and entered into the variable locations.
            if len(Alien.MoveBox.Ypositions) < Alien.Rows:
                Amount_of_Rows = len(Alien.MoveBox.Ypositions)
                for n in range(Amount_of_Rows, Alien.Rows):
                        Alien.MoveBox.Ypositions.append(-100*(n+1))
                        Alien.MoveBox.Rect = pygame.Rect((Alien.MoveBox.X, Alien.MoveBox.Ypositions[n]),(Alien.MoveBox.Width, Alien.MoveBox.Height))
                        Alien.MoveBox.Rects.append(Alien.MoveBox.Rect)
           
            for Box in range(len(Alien.MoveBox.Rects)):
                Alien.MoveBox.Rects[Box] = pygame.Rect((Alien.MoveBox.X, Alien.MoveBox.Ypositions[Box]),(Alien.MoveBox.Width, Alien.MoveBox.Height))

                #For every movement box the rectangle positions are moved depending on what position they are faceing and what the movement speed is.                 
                if Alien.MoveBox.Direction == "Left":
                    Alien.MoveBox.X -= Alien.MoveBox.MoveSpeed
                if Alien.MoveBox.Direction == "Right":
                    Alien.MoveBox.X += Alien.MoveBox.MoveSpeed
                    
                #If the box passes any side of the screen then the rows switch directions and move down by 10 pixels.
                if Alien.MoveBox.X > Screen.WIDTH - Alien.MoveBox.Width and Alien.MoveBox.Direction == "Right":
                    Alien.MoveBox.X = Screen.WIDTH - Alien.MoveBox.Width
                    for Pos in range(len(Alien.MoveBox.Rects)):
                        Alien.MoveBox.Ypositions[Pos]  += 10
                    Alien.MoveBox.Direction = "Left"
                
                if Alien.MoveBox.X < 0 and Alien.MoveBox.Direction == "Left":
                    Alien.MoveBox.X = 0
                    for Pos in range(len(Alien.MoveBox.Rects)):
                        Alien.MoveBox.Ypositions[Pos]  += 10
                    Alien.MoveBox.Direction = "Right"

                #If the aliens movebox toggle is enabled then it is drawn to the screen.
                if Alien.MoveBox.Toggle == True:
                    pygame.draw.rect(Screen.Window,RED,Alien.MoveBox.Rects[Box], 2)
                    
    def Reset(self):
        #Resets the lists and variables used by the alien.
        #Resets the lists used by the alien.
        self.Sprite_List = []
        self.Status_List = []
        self.Hitbox_List = []

        #States the gap between each alien in a row.
        self.Gap = 10

        #States how many rows are expected to be drawn.
        self.Rows = 4

        #Runs the other reset routines for the aliens.
        self.RowLists.Reset()
        self.MoveBox.Reset()
            
    def Setup(self):
        #Finds how many aliens can fit into the movement box then changes the size of the movement box to fit the aliens.
        Alien.Box = Alien.Type1.Sprite.get_rect()
        self.Alien_count = Alien.MoveBox.Width // (Alien.Box.width + Alien.Gap)
        Alien.MoveBox.Width = self.Alien_count * (Alien.Box.width + Alien.Gap) - (Alien.Gap*2)

        #The aliens lists are then filled using the different alien type data which are used on the appropriate rows.
        for RowNum in range (Alien.Rows):
            if RowNum > 3:
                RowNum = 0
                
            Alien.Sprite_List = []
            Alien.Status_List = []
            Alien.Hitbox_List = []
            Alien.Score_List = []
            
            for item in range(self.Alien_count):
                if RowNum <= 3:
                    Alien.Status_List.append("Alive")
                    
                if RowNum == 0:
                    Alien.Sprite_List.append(pygame.image.load(Alien.Type1.Image).convert_alpha())
                    Alien.Hitbox_List.append(Alien.Type1.Sprite.get_rect())
                    Alien.Score_List.append(100)
                    
                elif RowNum == 1:
                    Alien.Sprite_List.append(pygame.image.load(Alien.Type2.Image).convert_alpha())
                    Alien.Hitbox_List.append(Alien.Type2.Sprite.get_rect())
                    Alien.Score_List.append(200)
                    
                elif RowNum == 2:
                    Alien.Sprite_List.append(pygame.image.load(Alien.Type3.Image).convert_alpha())
                    Alien.Hitbox_List.append(Alien.Type3.Sprite.get_rect())
                    Alien.Score_List.append(300)
                    
                elif RowNum == 3:
                    Alien.Sprite_List.append(pygame.image.load(Alien.Type4.Image).convert_alpha())
                    Alien.Hitbox_List.append(Alien.Type4.Sprite.get_rect())
                    Alien.Score_List.append(400)
                
            Alien.RowLists.Sprites.append(Alien.Sprite_List[:])
            Alien.RowLists.Statuses.append(Alien.Status_List[:])
            Alien.RowLists.Hitboxes.append(Alien.Hitbox_List[:])
            Alien.RowLists.Scores.append(Alien.Score_List[:])
            
    def Position(self):
        #Checks if each alien to see if it has been destroyed or not. If it has not been destroyed then
        #the s=aliens are drawn to the screen. If not then they arent drawn to the screen. 
        Counter = 0
        for Box in range(len(Alien.MoveBox.Rects)):
            for item in range(len(Alien.RowLists.Hitboxes[Box])):
                if Alien.RowLists.Statuses[Box][item] == "Destroyed":
                    Counter+=1
                else:
                    Alien.RowLists.Hitboxes[Box][item].x =Alien.MoveBox.X + (item * (Alien.RowLists.Hitboxes[Box][item].width + Alien.Gap))
                    Alien.RowLists.Hitboxes[Box][item].y = Alien.MoveBox.Rects[Box].y
                    Screen.Window.blit(Alien.RowLists.Sprites[Box][item], (Alien.RowLists.Hitboxes[Box][item].x, Alien.RowLists.Hitboxes[Box][item].y))

                    #States that the game is over if the aliens pass the bottom of the screen.
                    if Alien.RowLists.Hitboxes[Box][item].y + Alien.Box.height > 534:
                        Game.OverToggle = True
                    
                    #States if the hitbox display is enabled then each aliens hit box is drawn to the screen.
                    if Alien.MoveBox.Toggle == True:
                        pygame.draw.rect(Screen.Window,RED, Alien.RowLists.Hitboxes[Box][item], 2)
                        
            #If every alien has been destroyed then the game increses the level and makes a new wave of aliens.            
            if Counter >= (self.Rows * self.Alien_count ):
                Alien.Reset()
                Alien.Setup()
                HUD.Level+= 1
                
    class Bullet:
        #States the bullet image variables
        Image = "Game Images/Sprites/Bullet.jpg"
        Sprite = pygame.image.load(Image)

        #States if the bullet is able to shoot
        Loaded = True

        def Reset():
            #Resets the Aliens gun
            Alien.Bullet.Loaded = True
            
        def Shoot():
            #Moves the aliens shot and deals with any of the collision of the bullets shot.
            #Moves the bullet if it has been shot and then draws it.
            if Alien.Bullet.Loaded == False:
                Alien.Bullet.Y += 3
                Screen.Window.blit(Alien.Bullet.Sprite, (Alien.Bullet.X, Alien.Bullet.Y))
                
                #If the bullet passes the bottom of the screen then the bullet is removed and the alien is able to shoot again.
                if Alien.Bullet.Y > 534:
                    Alien.Bullet.Loaded = True
                    
                #The alien hitbox is moved to the position the bullet should be so the collision can occur.
                Hitbox = Alien.Bullet.Sprite.get_rect()
                Hitbox.x = Alien.Bullet.X
                Hitbox.y = Alien.Bullet.Y

                #Then the collision with the player is checked. If it hits the player a life is lost and another shot is made available
                #for the alien.
                for item in Player.Hitbox:
                    if Hitbox.colliderect(item):
                        Alien.Bullet.Loaded = True
                        HUD.Lives -=1
            else:
                #If the alien bullet hasnt been shot then the aliens next start position is found and the alien shoots again.
                if len(Alien.MoveBox.Rects) > 0:
                    Randomer = random.randint(0, (len(Alien.MoveBox.Rects) - 1))
                    Alien.Bullet.Y = Alien.MoveBox.Rects[Randomer].y
                    Randomist = random.randint(0, (len(Alien.RowLists.Hitboxes[Randomer]) - 1))
                    Alien.Bullet.X = Alien.RowLists.Hitboxes[Randomer][Randomist].x
                    if Alien.RowLists.Statuses[Randomer][Randomist] == "Alive":
                        Alien.Bullet.Loaded = False
                
def Write_Text(Text, Font,Colour, X, Y, Distance_Apart, Area):
    #Lower cases the area variable to ensure its easier to program.
    Area = Area.lower()

    #for the lines in the given text
    for line in Text:
        #Defines the text ready for it to be drawn
        Render = Font.render(line, True, Colour)

        #Makes a positining rectangle
        Position = Render.get_rect()
        
        #Positions the texts y coordinate
        Position.centery = (Text.index(line) * Distance_Apart) + Y

        #Positions the texts x coordinate in the text box
        if Area == "center":
            Position.centerx = X
        else:
            Position.x = X

        #Draws the text to the screen
        Screen.Window.blit(Render, Position)
      
def Write_line(Text, Font,Colour, X, Y, Area):
    #Lower cases the area variable to ensure its easier to program.
    Area = Area.lower()

    #Defines the text ready for it to be drawn
    Render = Font.render(Text, True, Colour)

    #Makes a positining rectangle
    Position = Render.get_rect()
        
    #Positions the texts y coordinate
    Position.centery = Y

    #Positions the texts x coordinate in the text box
    if Area == "center":
        Position.centerx = X
    else:
        Position.x = X

    #Draws the text to the screen
    Screen.Window.blit(Render, Position)
        
class HUD:
    #States the location of the HUD border image to be drawn.
    Border_Image = "Game Images/UI/HUD box.png"

    #States the font used for the HUD.
    Font = pygame.font.SysFont('Agency FB', 30)
    
    def Reset(self):
        #Resets the games Live stats to the starting values.
        self.Score = 0
        self.Level = 1
        self.Lives = 3
    
    def Draw(self):
        #Draws the border image and the live data to the screen.
        self.Border = pygame.image.load(self.Border_Image).convert_alpha()
        self.Text = ("Level: " + str(self.Level) +
                     " Lives: " + str(self.Lives) +
                     " Score: " + str(self.Score) +
                     " HighScore: " + str(Stats.HighScore))
        Screen.Window.blit(self.Border, (0, 534))
        Write_line(self.Text, self.Font, WHITE, 400, 580, "Center")
        
class Stats:
    HighScore = 0
    
    def Load():
        #Loads the highscore from the external file
        HighScore_File = open("HighScore.txt", "r")
        for line in HighScore_File:
            Stats.HighScore = int(line)
        HighScore_File.close
        
    def Save():
        #Stores the highscore in the external file.
        HighScore_File = open("HighScore.txt", "w")
        HighScore_File.write(str(Stats.HighScore))
        HighScore_File.close

class PowerUps:
    #Store all of the information for the falling power ups.
    HitboxList = []
    SpriteList = []
    TypeList = []

    def Reset():
        #Resets the power ups
        PowerUps.HitboxList = []
        PowerUps.SpriteList = []
        PowerUps.TypeList =[]
        PowerUps.Timer.Start_Times = []
        PowerUps.Timer.Running = []
        PowerUps.Timer.Time = []
        PowerUps.Timer.Type = []
        
    class Timer:
        #Used to time the duration of the power ups used by the player.
        #Stores the starting time of each timer.
        Start_Times=[]
        #Stores how long the timer has been running for.
        Time = []
        #Holds whether the timer is running or not.
        Running = []
        #Stores the type of power up being dropped.
        Type =[]
        
        def Start(Time, Type):
            #Starts the timer for the power up depending on what type of power up it is.
            PowerUps.Timer.Start_Times.append(default_timer())
            PowerUps.Timer.Running.append(True)
            PowerUps.Timer.Time.append(Time)
            PowerUps.Timer.Type.append(Type)
            
        def Check():
            #Checks whether the duration of any of the timers running have ended. If they have then the power up ends
            #and the timer is removed from each list.
            if len(PowerUps.Timer.Running) > 0:
                for Timers in range(len(PowerUps.Timer.Running)):
                    duration = default_timer() - PowerUps.Timer.Start_Times[Timers]
                    if duration > PowerUps.Timer.Time[Timers]:
                        if PowerUps.Timer.Type[Timers] == 1:
                            Player.Bullet.Reload_Speed = 0.8
                        PowerUps.Timer.Start_Times.remove(PowerUps.Timer.Start_Times[Timers])
                        PowerUps.Timer.Running.remove(PowerUps.Timer.Running[Timers])
                        PowerUps.Timer.Time.remove(PowerUps.Timer.Time[Timers])
                        PowerUps.Timer.Check()
                        break
                    
    def Drop(AlienX,AlienY):
        #Randomises a power ups and places it in a location given ready for it to start dropping down.
        #Randomly picks the power up to be dropped.
        Randomiser = random.randint(0, 3)

        #1 Life
        if Randomiser == 0:
            ImagePos = "Game Images/Sprites/Power Ups/Powerups_Life.png"
        #Shoot Faster
        if Randomiser == 1:
            ImagePos = "Game Images/Sprites/Power Ups/Powerups_Fast Shoot.png"
        #500 points
        if Randomiser == 2:
            ImagePos = "Game Images/Sprites/Power Ups/Powerups_500.png"
        #1000 points
        if Randomiser == 3:
            ImagePos = "Game Images/Sprites/Power Ups/Powerups_1000.png"
            
        #Adds the data to the lists of data for the power up to be dropped.
        Image = pygame.image.load(ImagePos).convert_alpha()
        PowerUps.SpriteList.append(Image)
        Hitbox = Image.get_rect()
        Hitbox.x = AlienX
        Hitbox.y = AlienY
        PowerUps.HitboxList.append(Hitbox)
        PowerUps.TypeList.append(Randomiser)
        
    def Dropping():
        #Moves the power ups down the screen and performs actions when the power up collides with the player.
        #and destroys it self if it leaves the screen.
        if len(PowerUps.HitboxList) > 0:
            for Hitbox in range(len(PowerUps.HitboxList)):
                #Drops every power ups on screen down by 1 pixel and draws it.
                PowerUps.HitboxList[Hitbox].y += 1
                Screen.Window.blit(PowerUps.SpriteList[Hitbox],(PowerUps.HitboxList[Hitbox].x,PowerUps.HitboxList[Hitbox].y))

                #If the power up hits the player then the appropriate power up is given to the player.
                for P_Hitbox in Player.Hitbox:
                    if PowerUps.HitboxList[Hitbox].colliderect(P_Hitbox):
                        if PowerUps.TypeList[Hitbox] == 0:
                            if HUD.Lives < 5:
                                HUD.Lives += 1
                                
                        if PowerUps.TypeList[Hitbox] == 1:
                            Player.Bullet.Reload_Speed = 0.4
                            PowerUps.Timer.Start(5, PowerUps.TypeList[Hitbox])

                        if PowerUps.TypeList[Hitbox] == 2:
                            HUD.Score += 500

                        if PowerUps.TypeList[Hitbox] == 3:
                            HUD.Score += 1000

                #If the power up hits the player or the edge of the screen then the power up is removed from the lists and is eliminated.        
                    if PowerUps.HitboxList[Hitbox].colliderect(P_Hitbox) or PowerUps.HitboxList[Hitbox].y > Screen.HEIGHT:
                        PowerUps.HitboxList.remove(PowerUps.HitboxList[Hitbox])
                        PowerUps.SpriteList.remove(PowerUps.SpriteList[Hitbox])
                        PowerUps.TypeList.remove(PowerUps.TypeList[Hitbox])
                        PowerUps.Dropping()
                        return
                    
class Game:
    def Main_Menu():
        #Declares the background image location and background image to be used.
        Background_Image = "Game Images/UI/Information window Main menu.png"
        Background_Render = pygame.image.load(Background_Image).convert_alpha()
    
        #Declares the starting position of the menu selector
        Position = 0
    
        #Game loop
        while True:
            #Controls
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #If enter is pressed the option selected is run.
                    if event.key == K_RETURN:
                        #Runs the game
                        if Position == 0:
                            return
                        
                        #Opens the instructions
                        if Position == 1:
                            Game.Instructions()

                        #Quits the game
                        if Position == 2:
                            pygame.quit()
                            sys.exit()

                    #If up is pressed the selector moves up by one option.    
                    if event.key == K_UP or event.key == K_w:
                        Position -= 1

                    #If down is pressed the selector moves down by one option.
                    if event.key == K_DOWN or event.key == K_s:
                        Position += 1
                        
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                    #If the position of the selector goes past the last option it becomes the first option
                if Position > 2:
                    Position = 0

            #If the position of the selector goes past the first option it becomes the last option
                elif Position < 0:
                    Position = 2
                    
            #Animates the background    
            Background.Animate()
            
            #Draws the background to the screen       
            Screen.Window.blit(Background_Render,(150,73))

            #States the text which is used on the menu.
            Menu_Options_Text = ("Start",
                                 "Instructions",
                                 "Exit")
            HighScore_Text =("HighScore: " + str(Stats.HighScore))
            
            #Positions the pointer into the correct position depending on which option is highlighted.
            for item in range(len(Menu_Options_Text)):
                if Position == item:
                    PointerY = 300 + (item * 60)

            #Draws the information to the screen.    
            Font = pygame.font.SysFont('Agency FB', 30)
            Write_line(">", Font, GREEN, 200, PointerY, "Left")
            Write_line(HighScore_Text, Font, GREEN, 400, 20, "Center")
            Write_Text(Menu_Options_Text, Font,GREEN, 240, 300, 60, "Left")

            #Refreshes the screen image
            Screen.Refresh()
            
    def Instructions():
        #Declares the background image location and background image to be used.
        Background_Image = "Game Images/UI/Information window Main menu.png"
        Background_Render = pygame.image.load(Background_Image).convert_alpha()
    
        #Game loop
        while True:
            #Controls
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #If enter is pressed the game goes to the main menu.
                    if event.key == K_RETURN:
                        return
                    
                #Quits the game
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            #Animates the background    
            Background.Animate()
            
            #Draws the background to the screen       
            Screen.Window.blit(Background_Render,(150,73))

            #States the text which is used to inform people on how to play
            Instructions_Text = ("In Space invaders you must attempt to destroy as many aliens as",
                                 "you can before losing every life you have.The aliens slowly drop",
                                 "towards you and if they reach your ship you lose the game. The aliens",
                                 "will also shoot down deadly bullets which will remove 1 life if you",
                                 "are hit.",
                                 " ",
                                 "Controls:",
                                 "Move Left: Left arrow OR A",
                                 "Move Right: Right arrow OR D",
                                 "Shoot: Up arrow OR W OR SPACE")

            #Points awarded for each alien
            Points_Text = ("Green Alien = 100pts",
                           "Red Alien = 200pts",
                           "Yellow Alien = 300pts",
                           "Purple Alien = 400pts")

            #Text stating how to exit
            Exit_Prompt = "Press Enter to go back to the main menu."
            

            #Draws the information to the screen.    
            Font = pygame.font.SysFont('Agency FB', 18)
            Write_Text(Instructions_Text, Font,GREEN, 230, 250, 20, "Left")
            Write_Text(Points_Text, Font,GREEN, 430, 370, 20, "Left")
            Write_line(Exit_Prompt, Font, GREEN, 400, 460,"Center")
            
            #Refreshes the screen image
            Screen.Refresh()
            
    def InGame():
        #Performs all of the in game actions until the game is over.
        while True:
            Player.Controls()
            Background.Animate()
            Alien.MoveBox.Move()
            Alien.Position()
            Alien.Bullet.Shoot()
            Player.Bullet.Shooting()
            PowerUps.Dropping()
            PowerUps.Timer.Check()
            HUD.Draw()
            Background.Write_Prompt()
            Screen.Window.blit(Player.Sprite, (Player.X, Player.Y))
            
            #States that the Player hitbox should be drawn to the screen if the toggle is enabled.
            if Alien.MoveBox.Toggle == True:
                for P_Hitbox in Player.Hitbox:
                    pygame.draw.rect(Screen.Window, GREEN, P_Hitbox, 2)

            #If the fire variable is true the player shoots.    
            if Player.Bullet.Fire == True:
                Player.Bullet.Shoot()
                
            #If the life count goes below 0 the player loses.    
            if HUD.Lives <=0:
                Game.OverToggle = True

            #If the game is over the routine closes.
            if Game.OverToggle == True:
                break
            
            Screen.Refresh()
            
    def Pause():
        #Draws a prompt to the screen and stops all actions until the player leaves the screen.
        Windowbox = "Game Images/UI/Information window.png"
        windowboxy = pygame.image.load(Windowbox).convert_alpha()
        Game_OverFont = pygame.font.SysFont('Agency FB', 60)
        Font = pygame.font.SysFont('Agency FB', 30)
        Text = ["Game Paused", "Press \'esc\' to continue"]
        Screen.Window.blit(windowboxy, (150,84))
        Write_Text(Text, Font,GREEN, 400, 234, 40, "Center")
        Screen.Refresh()
            
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #If enter is pressed the option selected is run.
                    if event.key == K_ESCAPE:
                        return
                    
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
    def Over():
        #Draws a window to the screen displaying that the game is over and the Score they have achieved
        #and the level they have reached while giving them a prompt to go back to the main menu.
        Windowbox = "Game Images/UI/Information window.png"
        windowboxy = pygame.image.load(Windowbox).convert_alpha()
        Game_OverFont = pygame.font.SysFont('Agency FB', 60)
        Font = pygame.font.SysFont('Agency FB', 30)
        Text = []
        if HUD.Score > Stats.HighScore:
            Stats.HighScore = HUD.Score
            Text.append("NEW HIGHSCORE: " + str(HUD.Score))
        else:
            Text.append("Score: " + str(HUD.Score))
        Text.append("Level Reached: " + str(HUD.Level))    
        Text.append("Press Enter to continue")
        Screen.Window.blit(windowboxy, (150,84))
        Write_line("GAME OVER", Game_OverFont, RED, 400, 180, "Center") 
        Write_Text(Text, Font,RED, 400, 234, 40, "Center")
        Screen.Refresh()
        Loop = True
        
        while Loop == True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #If enter is pressed the option selected is run.
                    if event.key == K_RETURN:
                        Loop = False
                    
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        
    def Reset():
        #Resets all of the games values.
        Game.OverToggle = False
        Player.Respawn()
        Alien.Reset()
        Player.Bullet.Reset()
        PowerUps.Reset()
        Alien.Bullet.Reset()
        Alien.Setup()
        HUD.Reset()

#Main Code
Background = Background()
Screen = Screen()        
Screen.Setup()
Player = Player()
Alien = Alien()
Alien.Type1.init()
Alien.Type2.init()
Alien.Type3.init()
Alien.Type4.init()
HUD = HUD()

#Game Loop
while True:
    Game.Reset()
    Stats.Load()
    Game.Main_Menu()
    Game.InGame()
    Game.Over()
    Stats.Save()
