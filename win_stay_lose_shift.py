'''
Computational Models of Cognition
Final Project
11/14/18

Functions for implementing and running the Win-stay, lose-shift model in a replication study 
of Lee et al. (2011).
'''
import random
import numpy as np

class Game:

    def __init__(self, num_arms, gamma, environment):
        self.trial = 0
        self.arms = []
        self.num_arms = num_arms
        self.wins = 0
        self.gamma = gamma
        self.probabilities = self.get_arm_probabilities(environment)
        for i in range(num_arms):
            self.arms.append(self.probabilities[i])
            
    def get_total_rewards(self):
        '''
        Parameters: self
        Returns: A string listing the number of wins in the current game, the number of 
        losses in the current game, and the reward rate
        '''
        string = ""
        if self.trial != 0:
            string = "Total Wins: " + str(self.wins) + " ; Total Losses: " + str(self.trial - self.wins) + " ; Reward Rate:  " + str(self.wins / self.trial)
        else:
            string = "Trial zero."
        return string
    
    def get_arm_probabilities(self, environment):
        '''
        Parameters: 
            self
            environment: "n" for neutral, "s" for sparse, or "p" for plentiful
        Returns: a list of arm probabilities sampled from the corresponding Beta distributions 
        (Beta(1,1) for neutral; Beta(2,4) for sparse; Beta(4,2) for plentiful)
        '''
        probabilities = []
        for i in range(self.num_arms):
            if environment == "n":
                probabilities.append(np.random.beta(1,1))
            elif environment == "s":
                probabilities.append(np.random.beta(2,4))
            else:
                probabilities.append(np.random.beta(4,2))
        return probabilities

    
def switch_arm(game, arm):
    '''
    Parameters: 
        game: a game object
        arm: an int referring to an arm
    Returns: an int representing a random different arm
    '''

    new_arm = arm
    while new_arm == arm:
        new_arm = random.randint(0, game.num_arms - 1)
    return new_arm


def win_stay_lose_shift(previous_trial, game):
    '''
    Implements win-stay lose-shift heuristic

    Parameters: 
        previous trial: a tuple containing the previous choice and its result (win or loss)
            previous choice is a number, 0 or 1, associated with which arm (option) is chosen
            previous trial result is a number associated with whether the trial won or lost. 
            0 for loss; 1 for win
        gamma: the probability of switching when you lose and staying when you win

    Returns: a tuple that contains this trial's choice and result
    '''
    next_choice = decide_next_move(game, previous_trial)
    result = calculate_result(next_choice, game)
    return (next_choice, result)
    
    
def decide_next_move(game, previous_trial):
    '''
        Decides which arm to choose next depending on which arm was chosen previously and what the result was
        
        Parameters: 
            game: the game object
            previous trial: a tuple containing previous choice and result
        
        Returns: an integer associated with which arm will be chosen next
    '''
    
    switch_number = random.random()
    #If the last trial was a win, stay gamma percent of the time
    if previous_trial[1] == 1 and switch_number <= game.gamma: 
        return previous_trial[0] #return the same arm
    #If the last trial was a win, switch 1-gamma percent of the time
    elif previous_trial[1] == 1 and switch_number > game.gamma: 
        #Identify which arm the last guess used and switch it
        return switch_arm(game, previous_trial[0])
    #If the last trial was a loss, switch gamma percent of the time
    elif previous_trial[1] == 0 and switch_number <= game.gamma: 
        return switch_arm(game, previous_trial[0])
    #If last trial was a loss, stay 1-gamma percent of the time
    else: 
        return previous_trial[0]

    
def calculate_result(choice, game):
    '''
    Calculates the outcome of the choice (a win or loss) based on the probabilities associated with each arm.

    Parameters: 
        choice: the choice of arm
        game: the game object being played, which holds the probabilities of success for the arms

    Returns: int outcome (0 if loss, 1 if win)
    '''
    win_number = random.random()
    
    #Probability of success for the chosen arm
    prob_success = game.arms[choice]
    
    game.trial += 1
    if win_number <= prob_success:
        game.wins += 1
        return 1
    else:
        return 0


def run_win_stay_simulation(n, trials, choices_filename, results_filename, num_arms, gamma, environment):
    '''
    Parameters: 
        n: number of games
        trials: number of trials for each game
        choices_filename: file to be created and written with choice data
        results_filename: file to be created and written with results data
        num_arms: number of arms in the game
        gamma: a value for gamma
        environment: "n" for neutral, "s" for sparse, "p" for plentiful

    Writes outcome of simulation to a file in .csv format.
    '''
    choices_file = open(choices_filename, "w")
    results_file = open(results_filename, "w")
    
    #Write a header
    for h in range(trials):
        choices_file.write("trial" + str(h) + "choice")
        results_file.write("trial" + str(h) + "result")
        if h < trials - 1:
            choices_file.write(",")
            results_file.write(",")
            
    #Initialize and run n games
    for i in range(n):
        game = Game(num_arms, gamma, environment)
        choices_file.write("\n")
        results_file.write("\n")
        
        first_choice = random.randint(0, num_arms-1)
        first_result = calculate_result(first_choice, game)
        trial =(first_choice, first_result)
        
        #Run trials for each game        
        for j in range(trials):
            trial = win_stay_lose_shift(trial, game)
            choices_file.write(str(trial[0]))
            results_file.write(str(trial[1]))
            #Write a comma after the result if the trial is not the last trial
            if j < trials - 1:
                choices_file.write(",")
                results_file.write(",")
            
            
def generate_model_data():
    '''
    Run the Win-stay, lose-shift model in neutral, sparse, and plentiful environments with 
    parameters chosen for our experiment.
    '''
    #Neutral environment
    run_win_stay_simulation(500, 8, "./ModelData/WSLS/WSLSNeutral8Choices.csv", "./ModelData/WSLS/WSLSNeutral8Results.csv", 2, .9, "n")
    run_win_stay_simulation(500, 16, "./ModelData/WSLS/WSLSNeutral16Choices.csv", "./ModelData/WSLS/WSLSNeutral16Results.csv", 2, .9, "n")
    
    #Sparse environment
    run_win_stay_simulation(500, 8, "./ModelData/WSLS/WSLSSparse8Choices.csv", "./ModelData/WSLS/WSLSSparse8Results.csv", 2, .9, "s")
    run_win_stay_simulation(500, 16, "./ModelData/WSLS/WSLSSparse16Choices.csv", "./ModelData/WSLS/WSLSSparse16Results.csv", 2, .9, "s")
    
    #Plentiful environment
    run_win_stay_simulation(500, 8, "./ModelData/WSLS/WSLSPlentiful8Choices.csv", "./ModelData/WSLS/WSLSPlentiful8Results.csv", 2, .9, "p")
    run_win_stay_simulation(500, 16, "./ModelData/WSLS/WSLSPlentiful16Choices.csv", "./ModelData/WSLS/WSLSPlentiful16Results.csv", 2, .9, "p")
    
#generate_model_data()