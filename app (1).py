from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import time
from subprocess import call

# Import the AllinOneGA script
from geneticAlgo import initializeChromosome, fitnessFunction, separateChromosome

def call_genetic():
    call(['python','GeneticAlgo.py'])

app = Flask(__name__)

@app.route('/')
def index():
    # # Generate a chromosome
    # chromosome = initializeChromosome()
    # # Calculate fitness
    # fitness = fitnessFunction(chromosome)
    # # Separate the chromosome data
    # sem2, sem4, sem6, sem8 = separateChromosome(chromosome)
    
    # Send the data to the frontend
    return render_template('index.html', sem2=sem2, sem4=sem4, sem6=sem6, sem8=sem8, fitness=fitness)

if __name__ == "__main__":
    app.run(debug=True)
