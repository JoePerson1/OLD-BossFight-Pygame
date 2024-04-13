import pygame

# highscores do not save after respawns

# settings
bgX = 1200
bgY = 800
gracePeriod = 1000
defaultLives = 3

class NotSquare(pygame.sprite.Sprite):
  def __init__(self, picture, x, y, speed, scale):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(picture).convert_alpha()
    self.image = pygame.transform.scale(self.image, scale)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.speed = speed
    self.decimal = pygame.math.Vector2([self.rect.centerx,
                                        self.rect.centery])
    self.default = self.rect.center
    
class Square(pygame.sprite.Sprite):
  def __init__(self, color, x, y, width, height):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((width, height))
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    
class Boss(NotSquare):
  def __init__(self, picture, x, y, speed, scale):
    super().__init__(picture, x, y, speed, scale)
    
  def cleave(self):
    global bossCount
    global stillCharacterPos
    cleaveSpeed = 50
    cleaveCooldown = 15
    if bossCount % cleaveCooldown == 0:
      stillCharacterPos = character.rect.center
      self.decimal = follow(stillCharacterPos, self.rect.center, cleaveSpeed,
                            self.decimal, True)
      sword = NotSquare('sword.png', self.rect.centerx,
                        self.rect.centery, None, (15, 50))
    bossCount += 1
    if bossCount % (2*cleaveCooldown) > cleaveCooldown:
      self.rect.center = [self.rect.center[0]+self.decimal[0],
                          self.rect.center[1]+self.decimal[1]]
    
def start():
  global score
  global lives
  lives = defaultLives
  score = 0
  character.rect.center = character.default
  enemy.rect.center = enemy.default
  enemy.decimal = enemy.default

def follow(characterPos, followerPos, speed, coords, doVector):
  characterVector = pygame.math.Vector2(characterPos)
  followerVector = pygame.math.Vector2(followerPos)
  coords -= followerVector
  distance = characterVector - followerVector
  try:
    directionVector = pygame.math.Vector2.normalize(distance)
    followerVector2 = followerVector + directionVector * speed
  except:
    directionVector = pygame.math.Vector2([0, 0])
    followerVector2 = followerVector
  if doVector:
    return directionVector.x*speed, directionVector.y*speed
    
  return followerVector2.x+coords.x, followerVector2.y+coords.y

pygame.init()
screen = pygame.display.set_mode((bgX, bgY))
pygame.display.set_caption('Dodge')
clock = pygame.time.Clock()

backboardHeight = bgY//10

score = 0
backboardTop = Square('black', bgX//2, backboardHeight//2, bgX, backboardHeight)
scoreFont = pygame.font.Font(None, 3*(backboardTop.rect.centery//2))
backboardBottom = Square('black', bgX//2, (19/2)*backboardHeight, bgX, backboardHeight)

x = 50
livesGroup = pygame.sprite.Group()
for i in range(defaultLives):
  x += 30
  heart = NotSquare('heart.png', x, (19/2)*backboardHeight, 1, (65, 60))
  livesGroup.add(heart)
  print(livesGroup)
livesGroup.draw(screen)

background = NotSquare('background final.png', 1000, backboardTop.rect.centery,
                    1, (5*(bgY-(2*backboardHeight)), bgY-(2*backboardHeight)))
character = NotSquare('character.png', bgX//8, bgY//2, 5, (20, 20))
enemy = Boss('enemy1.png', 6*(bgX//8), bgY//2, 2, (50, 50))

start()

bossCount = 0
respawns = 0
cooldown = 0
dash = False
defaultSpeed = 5
character.speed = defaultSpeed
ticks1 = 0
lastMove = None
run = True
alive = True
Efollow = True
count = 0
moves = ['sickle', '']
grace = False
liveCheck = 0

r = open('highscore.txt', 'r')
highscore = r.readlines()[0]
r.close()

while run:
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if lastMove == event.key:
        ticks1 = pygame.time.get_ticks()
      lastMove = event.key
      if event.key == pygame.K_RETURN and not alive:
        start()
        alive = True
        respawns = 0
      elif event.key == pygame.K_BACKSPACE and not alive:
        grace = True
        graceTime = 0
        alive = True
        lives -= 1
      
  if alive:
    character.rect.left += (keys[pygame.K_d] - keys[pygame.K_a])*character.speed
    character.rect.top += (keys[pygame.K_s] - keys[pygame.K_w])*character.speed
    
    if character.rect.left < 0: character.rect.left = 0
    if character.rect.right > bgX: character.rect.right = bgX
    if character.rect.top < backboardTop.rect.bottom: character.rect.top = backboardTop.rect.bottom
    if character.rect.bottom > bgY: character.rect.bottom = bgY
    
    if not dash:
      ticks2 = pygame.time.get_ticks()
      if ticks2 - ticks1 < 20:
        if not cooldown:
          character.speed = 30
          dash = True
          count2 = count
        cooldown = True
    elif dash:
      if pygame.time.get_ticks() - ticks2 > 100:
        character.speed = defaultSpeed
        dash = False
        
    if cooldown:
      if count-count2 >= 120:
        cooldown = False
    
    if Efollow:
      enemy.decimal = follow(character.rect.center, enemy.rect.center, 3,
                             enemy.decimal, False)
      enemy.rect.center = enemy.decimal
    
    Efollow = False
    enemy.cleave()
    
    print(enemy.rect.center)
    
    count += 1
    if count % 12 == 0:
      score += 5
    
    screen.blit(backboardTop.image, backboardTop.rect)
    screen.blit(backboardBottom.image, backboardBottom.rect)
    scoreDisplay = scoreFont.render('Score: ' + str(score), False, 'white')
    scoreWidth = scoreDisplay.get_width()
    
    if not grace and character.rect.colliderect(enemy.rect):
      alive = False
      r = open('highscore.txt', 'r')
      if int(r.readlines()[0]) < score and lives > 0:
        highscore = score
        w = open('highscore.txt', 'w')
        w.write(str(score))
        r.close()
        w.close()
      print('Score: ' + str(score))
      print('Lives Left: ' + str(lives - 1))
      print('Highscore: ' + str(highscore))
      print()
      
    if grace:
      graceTime += 1
      if graceTime == gracePeriod * 60:
        grace = False
      
    if count % ((.2*background.image.get_width())/background.speed) == 0:
      background.rect.centerx = 1000
    
    background.rect.centerx -= background.speed
    screen.blit(background.image, (background.rect.left, backboardTop.rect.bottom))
    screen.blit(character.image, character.rect)
    screen.blit(enemy.image, enemy.rect)
    screen.blit(scoreDisplay, (.5*(bgX-scoreWidth), backboardTop.rect.centery//2))
    
    pygame.display.update()
    clock.tick(60)
    