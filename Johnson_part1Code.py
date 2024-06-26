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
   
        
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Campus.jpg")
        
        self.sndCoin = simpleGE.Sound("coin.wav")
        self.sndHurt = simpleGE.Sound("lose sound 2 - 1_0.wav")
        self.numCoins = 5
        self.numHurts = 3
        
        self.charlie = Charlie(self)
        
        self.coins = []
        self.hurts = []
        
        for i in range(self.numCoins):
            self.coins.append(Coin(self))
        for i in range(self.numHurts):
            self.hurts.append(Hurt(self))

        self.sprites = [self.charlie, self.coins, self.hurts]
    
    def process(self):
        for coin in self.coins:
            if coin.collidesWith(self.charlie):
                coin.reset()
                self.sndCoin.play()
        for hurt in self.hurts:
            if hurt.collidesWith(self.charlie):
                hurt.reset()
                self.sndHurt.play()

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
                
   
        
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":    
    main()
