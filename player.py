import random
import pygame
import config
import brain
import pickle

class Player:
    def __init__(self):
        # Bird
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0
        self.pipesPassed = 0

        # Ai
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def draw(self, window):
        # Draw the tinted image within the player's rect area
        #pygame.draw.rect(window, self.color, self.rect)

        # UNCOMMENT IF YOU WANT FLYING PENISES
        resized_flying_image = pygame.transform.scale(pygame.image.load("bird.png"), (50, 50))
        window.blit(resized_flying_image, (self.rect.topleft[0] - 20, self.rect.topleft[1] - 20))


    def ground_collision(self,ground):
        return pygame.Rect.colliderect(self.rect,ground)
    
    def sky_collision(self):
        return bool(self.rect.y < 30)
    
    def pipe_collision(self):
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect,p.top_rect) or \
                   pygame.Rect.colliderect(self.rect,p.bottom_rect)
    
    def update(self,ground):
        if not(self.ground_collision(ground) or self.pipe_collision()):
            #gravity
            self.vel += 0.25
            self.rect.y+=self.vel
            if self.vel > 5:
                self.vel = 5
            #Incrament a life span
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0
    
    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= 1:#Possibly tweak this
            self.flap = False

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p
    
    def score(self):
        done = False
        for p in config.pipes:
            if p.passed and not done:
                self.pipesPassed += 1/50

    def look(self):#Could use on graph for all of the inputs
        if config.pipes:
            #line to top pipe
            self.vision[0] = max(0,self.rect.center[1] - self.closest_pipe().top_rect.bottom)/500
            pygame.draw.line(config.window, self.color, self.rect.center, 
                             (self.rect.center[0], config.pipes[0].top_rect.bottom))
            
            #line to mid pipe
            self.vision[1] = max(0,self.closest_pipe().x - self.rect.center[0])/500
            pygame.draw.line(config.window, self.color, self.rect.center, 
                             (config.pipes[0].x, self.rect.center[1]))
            
            #line to bottom pipe
            self.vision[2] = max(0,self.closest_pipe().bottom_rect.top - self.rect.center[1])/500
            pygame.draw.line(config.window, self.color, self.rect.center, 
                             (self.rect.center[0], config.pipes[0].bottom_rect.top))
        
    #AI related Functions
    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone
    
    def save_genome(player, filename):
        genomes = {}
        # Load existing genomes
        try:
            with open(filename, 'rb') as f:
                genomes = pickle.load(f)
        except:
            pass  # if file doesn't exist yet or empty
        
        # Add the new genome with a unique identifier
        identifier = str(len(genomes) + 1)  # this can be a timestamp or anything unique
        genomes[identifier] = player.brain
        
        with open(filename, 'wb') as f:
            pickle.dump(genomes, f)
            
        return identifier  # return the identifier for the user to know

    # in player.py
    def load_genome(filename, identifier):
        with open(filename, 'rb') as f:
            genomes = pickle.load(f)
            if identifier in genomes:
                return genomes[identifier]
            else:
                raise ValueError("Genome with identifier {} not found.".format(identifier))

