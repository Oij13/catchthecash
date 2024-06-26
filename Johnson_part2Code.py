# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:35:34 2024

@author: cmj17
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:00:06 2024

@author: owen.johnson3
"""

import pygame, simpleGE, random

class Charlie(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Charlie.png")
        self.setSize(50, 50)
        self.position = (320, 400)
        self.moveSpeed = 5
        self.inAir = True
   
        
        
    def process(self):
        if self.isKeyPressed(pygame.K_a):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_d):
            self.x += self.moveSpeed
       
        if self.inAir:
            self.addForce(.2,270)
            
        if self.y > 400:
            self.inAir = False
            self.y = 400
            self.dy = 0
            
            
        if self.scene.isKeyPressed(pygame.K_SPACE) or self.isKeyPressed(pygame.K_w):
            self.dy = 0
            self.addForce(5,90)
            if not self.inAir:
                self.addForce(6,90)
                self.inAir = True 
        

            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 10"
        self.center = (500, 30)
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Campus.jpg")
        
        self.sndCoin = simpleGE.Sound("coin.wav")
        self.sndHurt = simpleGE.Sound("lose sound 2 - 1_0.wav")
        self.numCoins = 5
        self.numHurts = 5
        self.score = 0
        self.lblScore = LblScore()
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.lblTime = LblTime()
        
        pygame.mixer.music.load("Daisy.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(-1)
        
        self.charlie = Charlie(self)
        
        self.coins = []
        self.hurts = []
        
        for i in range(self.numCoins):
            self.coins.append(Coin(self))
        for i in range(self.numHurts):
            self.hurts.append(Hurt(self))

        self.sprites = [self.charlie, 
                        self.coins, 
                        self.hurts,
                        self.lblScore,
                        self.lblTime]
    
    def process(self):
        for coin in self.coins:
            if coin.collidesWith(self.charlie):
                coin.reset()
                self.sndCoin.play()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        for hurt in self.hurts:
            if hurt.collidesWith(self.charlie):
                hurt.reset()
                self.sndHurt.play()
                if self.score > 0:
                    self.score -= 1
                self.lblScore.text = f"Score: {self.score}"
        self.lblTime.text = f"Time left: {self.timer.getTimeLeft():.2}"
        
        if self.timer.getTimeLeft() < 0:
            print(f"Score: {self.score}")
            self.stop()
class Coin(simpleGE.Sprite):
    
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Coin.png")
        
        self.setSize(25, 25)
        self.minSpeed = 3 
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, 640)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
        
    def checkBounds(self):
        if self.bottom > self.screen.get_height():
            self.reset()
        
class Hurt(simpleGE.Sprite):
    
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("BadCloud.png")
        
        self.setSize(25, 25)
        self.minSpeed = 3 
        self.maxSpeed = 6
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, 640)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
        
    def checkBounds(self):
        if self.bottom > self.screen.get_height():
            self.reset()
                


class Instruction(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        self.setImage("campus.jpg")
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are Ball State's mascot",
        "Move character with the left and right arrow keys",
        "Catch as much cash as you can",
        "Avoid the clouds or lose points",
        "Press space to jump",
        "Good Luck and try to beat your last score!"]
        
        self.directions.center = (320, 240)
        self.directions.size = (500, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (W)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last Score: 0"
        self.lblScore.center = (320, 400)
        
        self.lblScore.text = f"Last Score: {self.prevScore}"
        
        pygame.mixer.music.load("Daisy.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(-1)
        
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
        
        
    def process(self):
        if self.btnPlay.clicked or self.isKeyPressed(pygame.K_w):
            self.response = "Play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
    
        
        
def main():
    keepGoing = True
    lastScore = 0
    while keepGoing:
        
        instructions = Instruction(lastScore)
        
        instructions.start()
        if instructions.response == "Play" :
            game = Game()
            game.start()
            lastScore = game.score
        else:
            keepGoing = False
    
if __name__ == "__main__":    
    main()
