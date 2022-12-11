import pygame
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing=True
        self.hitbox= (self.x+17,self.y+11,29,52)
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox= (self.x+17,self.y+11,29,52)

        #pygame.draw.rect(win, (255,0,0),self.hitbox,2)
    def hit(self):
        self.isJump= False
        self.jumpCount=10
        self.x = 100 # We are resetting the player position
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

def redrawGameWindow():
    win.blit(bg, (0,0))
    zizo.draw(win)
    terrorist.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (39, 10))
    pygame.display.update()

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox= (self.x+17,self.y+11,29,52)
        self.health = 10 
        self.visible = True 

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33: # Since we have 11 images for each animtion our upper bound is 33.   # We will show each image for 3 frames. 3 x 11 = 33.
                self.walkCount = 0
                
            if self.vel > 0: # If we are moving to the right we will display our walkRight images
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:  # Otherwise we will display the walkLeft images
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            self.hitbox= (self.x+17,self.y+11,29,52)
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) # NEW
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10)) # NEW
            #self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        #pygame.draw.rect(win, (255,0,0),self.hitbox,2)
    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x < self.path[1] + self.vel: # If we have not reached the furthest right point on our path.
                self.x += self.vel
            else: # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else: # If we are moving left
            if self.x > self.path[0] - self.vel: # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    def hit(self):
       # hitSound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')
                
#mainloop
zizo = player(200, 410, 64,64)
terrorist=enemy(100,410,64,64,450)
run = True
bullets=[]
shootLoop=0
score=0
font = pygame.font.SysFont("comicsans", 30, True)
# bulletSound = pygame.mixer.music.load("bullet.mp3")
# hitSound = pygame.mixer.music.load("hit.mp3")

#     

while run:
    clock.tick(27)
    if terrorist.visible==True:
        if zizo.hitbox[1] < terrorist.hitbox[1] + terrorist.hitbox[3] and zizo.hitbox[1] + zizo.hitbox[3] > terrorist.hitbox[1]:
            if zizo.hitbox[0] + zizo.hitbox[2] > terrorist.hitbox[0] and zizo.hitbox[0] < terrorist.hitbox[0] + terrorist.hitbox[2]:
                zizo.hit()
                score -= 5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    for bullet in bullets:
        if bullet.y - bullet.radius < terrorist.hitbox[1] + terrorist.hitbox[3] and bullet.y + bullet.radius > terrorist.hitbox[1]: # Checks x coords
             if bullet.x + bullet.radius > terrorist.hitbox[0] and bullet.x - bullet.radius < terrorist.hitbox[0] + terrorist.hitbox[2]: # Checks y coords
                    terrorist.hit() # calls enemy hit method
                    score += 1
                    bullets.pop(bullets.index(bullet)) # removes bullet from bullet list 
        if bullet.x<500 and bullet.x>0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop == 0:#
        #bulletSound.play()

        if zizo.left:
            facing=-1
        else:
            facing=1
        if len(bullets)<5:
            bullets.append(projectile(round(zizo.x+zizo.width//2), round(zizo.y + zizo.height//2), 6, (0,0,0), facing))
        shootLoop=1
    if keys[pygame.K_LEFT] and zizo.x > zizo.vel:
        zizo.x -= zizo.vel
        zizo.left = True
        zizo.right = False
        zizo.standing= False
    elif keys[pygame.K_RIGHT] and zizo.x < 500 - zizo.width - zizo.vel:
        zizo.x += zizo.vel
        zizo.right = True
        zizo.left = False
        zizo.standing= False

    else:
        zizo.standing=True
        zizo.walkCount = 0
        
    if not(zizo.isJump):
        if keys[pygame.K_UP]:
            zizo.isJump = True
            zizo.right = False
            zizo.left = False
            zizo.walkCount = 0
    else:
        if zizo.jumpCount >= -10:
            neg = 1
            if zizo.jumpCount < 0:
                neg = -1
            zizo.y -= (zizo.jumpCount ** 2) * 0.5 * neg
            zizo.jumpCount -= 1
        else:
            zizo.isJump = False
            zizo.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()