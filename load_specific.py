import pygame
from sys import exit
import config
import components
from player import Player

pygame.init()
clock = pygame.time.Clock()

# Load the genome and create a player with it
loaded_genome = Player.load_genome('SavedGameInfo.txt','4')
player_with_saved_genome = Player()
player_with_saved_genome.brain = loaded_genome

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    pipes_spawn_time = 10
    while True:
        quit_game()

        config.window.fill((135,206,235))

        # Spawning ground
        config.ground.draw(config.window)

        # Update the player's vision
        player_with_saved_genome.look()

        # Let the player think based on the current vision
        player_with_saved_genome.think()

        # Spawning pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        # Draw and update the pipes
        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)
        
        # Update the player_with_saved_genome
        if player_with_saved_genome.alive:
            player_with_saved_genome.score()
            player_with_saved_genome.draw(config.window)
            player_with_saved_genome.update(config.ground)
        else:
            config.pipes.clear()
            # You can decide what to do here, e.g., end the game or restart

        clock.tick(60)
        pygame.display.flip()

main()
