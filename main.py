import pygame
from sys import exit
import config
import components
import population
from player import Player
from graph import *

pygame.init()
clock = pygame.time.Clock()
#Spawning one player
population = population.Population(50)

#Graphing
f = open('SavedGameInfo.txt','r')

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    pipes_spawn_time = 10
    tick_counter = 0  # Initialize tick counter
    
    # Initialize data collection for graphing
    all_generations_data = []
    current_generation = 1

    while True:
        quit_game()

        config.window.fill((135,206,235))

        # Spawning ground
        config.ground.draw(config.window)

        # Spawning pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        # Draws and updates the pipes
        for p in config.pipes:
            p.draw(config.window)
            p.update()
            if p.off_screen:
                config.pipes.remove(p)

        if not population.extinct():
            population.update_live_players()
        else:
            # Reset tick_counter when population goes extinct
            tick_counter = 0
            
            # Collect and store weight vs. fitness data after each generation
            current_gen_data = []
            for player in population.players:
                for connection in player.brain.connections:
                    current_gen_data.append((connection.weight, player.fitness))
            all_generations_data.append(current_gen_data)
            
            # Plot the data for the current generation
            plot(current_gen_data, current_generation)

            current_generation += 1
            config.pipes.clear()
            population.natural_selection()

        # Check the survival duration for the entire population
        tick_counter += 1
        if tick_counter >= 1000:  # Population survived for 1000 ticks
            # Save the genomes of only the alive players in the population
            for player in population.players:
                if player.alive:  # Check if the player is still alive
                    Player.save_genome(player, 'SavedGameInfo.txt')  # This will need to be modified if you want multiple saves in one file
                for connection in player.brain.connections:
                    current_gen_data.append((connection.weight, player.fitness))
            all_generations_data.append(current_gen_data)
            plot_all_generations_with_trendline(all_generations_data)
            plot_histogram(all_generations_data)
            plot_fitness_histogram(all_generations_data)
            pygame.quit()
            exit()

        clock.tick(60)
        pygame.display.flip()

main()

