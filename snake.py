import pygame
import random

pygame.init()
WIDTH, HEIGHT = 600, 400
SQUARE_SIZE = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Classes")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS=10

class Snake:
    '''
    a snake can display,move,grow,change direction,dead
    '''
    def __init__(self):
        self.body = [[100, 50], [80, 50], [60, 50]]
        self.direction = "RIGHT"
        self.head = self.body[0]
    def draw(self,window):
        for segment in self.body:
            pygame.draw.rect(window, BLUE, [segment[0], segment[1], SQUARE_SIZE, SQUARE_SIZE])
    def move(self):
        x,y=self.head
        if self.direction == "UP":
            y-=SQUARE_SIZE
        if self.direction == "DOWN":
            y+= SQUARE_SIZE
        if self.direction == "LEFT":
            x-= SQUARE_SIZE
        if self.direction == "RIGHT":
            x+= SQUARE_SIZE
        new=[x,y]
        self.body.insert(0, new)
        self.body.pop()
        self.head = self.body[0]
    def grow(self):
         self.body.append(self.body[-1])
    def changedrt(self,direction):
        if direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        if direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
class Food:
    def __init__(self):
        self.pos=self.randpos()
    def randpos(self):
        x=random.randrange(0, WIDTH // SQUARE_SIZE) * SQUARE_SIZE
        y=random.randrange(0, HEIGHT // SQUARE_SIZE) * SQUARE_SIZE
        return[x,y]
    def repos(self):
        self.pos=self.randpos()
    def draw(self, window):
        pygame.draw.rect(window, GREEN, [self.pos[0], self.pos[1], SQUARE_SIZE, SQUARE_SIZE])
    def eliminate(self):
        self.pos = [-SQUARE_SIZE, -SQUARE_SIZE]
    def draw_again(self,window):
        self.repos()
        pygame.draw.rect(window, GREEN, [self.pos[0], self.pos[1], SQUARE_SIZE, SQUARE_SIZE])
class Snakegame:
    '''this game includes draw elements,check collision,game loop,game over'''
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0
    def reset(self):
        self.snake=Snake()
        self.food=Food()
        self.running = True
        self.score = 0
    def draw(self):
        WIN.fill(WHITE)
        self.snake.draw(WIN)
        self.food.draw(WIN)
        font = pygame.font.SysFont("bahnschrift", 25)
        score_text = font.render(f"Score: {self.score}", True, BLUE)
        WIN.blit(score_text, [10, 10])
        pygame.display.update()
    def check(self):
        '''check if there's collision'''
        # collision with food
        if self.snake.head==self.food.pos:
            self.snake.grow()
            self.food.pos=self.food.repos()
            self.food.eliminate()
            self.food.draw_again(WIN)
            self.score+=1
            self.food.draw(WIN)
        # collision with self or the wall
        if (self.snake.head[0] < 0 or self.snake.head[0] >= WIDTH or self.snake.head[1] < 0 or self.snake.head[1] >= HEIGHT or self.snake.head in self.snake.body[1:]):
            self.running = False
    def gameloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
            # get keyboard input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.snake.changedrt("UP")
            if keys[pygame.K_DOWN]:
                self.snake.changedrt("DOWN")
            if keys[pygame.K_LEFT]:
                self.snake.changedrt("LEFT")
            if keys[pygame.K_RIGHT]:
                self.snake.changedrt("RIGHT")
            self.snake.move()
            self.check()
            if self.running:
                self.draw()
            self.clock.tick(FPS)
        self.gameover()
    def gameover(self):
        WIN.fill(BLACK)
        font = pygame.font.SysFont("bahnschrift", 35)
        msg = font.render("Game Over! Press R to Restart or Q to Quit", True, RED)
        WIN.blit(msg, [WIDTH // 8, HEIGHT // 3])
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        self.gameloop()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

if __name__ == "__main__":
    game = Snakegame()
    game.gameloop() 