import matplotlib.pyplot as plt
import numpy as np

def plot(data, generation_number):
    weights, fitness_values = zip(*data)
    plt.figure(f"Generation {generation_number}")
    plt.scatter(weights, fitness_values, alpha=0.5)
    plt.title(f"Generation {generation_number}: Weights vs. Fitness")
    plt.xlabel('Weights')
    plt.ylabel('Fitness')
    plt.show()

def plot_all_generations_with_trendline(all_generations_data):
    # Flatten the data across all generations into one list
    all_data = [item for sublist in all_generations_data for item in sublist]
    weights, fitness_values = zip(*all_data)
    
    plt.figure(figsize=(12, 6))
    plt.scatter(weights, fitness_values, alpha=0.5, label='Data')

    # Compute and plot trendline
    z = np.polyfit(weights, fitness_values, 1)
    p = np.poly1d(z)
    plt.plot(weights, p(weights), "r-", label=f'Trendline: y={z[0]:.2f}x+{z[1]:.2f}')
    
    plt.title('All Generations: Weights vs. Fitness')
    plt.xlabel('Weights')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()

def plot_histogram(all_generations_data):
    # Flatten all weights from all generations into a single list
    all_weights = [weight for generation in all_generations_data for weight, _ in generation]
    
    plt.figure(figsize=(10, 6))
    plt.hist(all_weights, bins=20, color='blue', alpha=0.7, edgecolor='black')
    
    plt.title('Distribution of Weights over All Generations')
    plt.xlabel('Weight Value')
    plt.ylabel('Frequency')
    
    plt.show()

def plot_fitness_histogram(all_generations_data):
    # Flatten all fitness values from all generations into a single list
    all_fitness_values = [fitness for generation in all_generations_data for _, fitness in generation]
    
    plt.figure(figsize=(10, 6))
    plt.hist(all_fitness_values, bins=50, color='green', alpha=0.7, edgecolor='black')
    
    plt.title('Distribution of Fitness Values over All Generations')
    plt.xlabel('Fitness Value')
    plt.ylabel('Frequency')
    
    plt.show()