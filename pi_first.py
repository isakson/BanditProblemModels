'''
Computational Models of Cognition
Final Project
11/14/18

Functions for implementing and running the Pi-First model in a replication study 
of Lee et al. (2011).
'''
import random
import numpy as np

class Game:
    
    def __init__(self, num_arms, pi, gamma, environment):
        self.trial = 0
        self.arms = []
        self.num_arms = num_arms
        self.pi = pi
        self.gamma = gamma
        self.probabilities = self.get_arm_probabilities(environment)

        for i in range(num_arms):
            temp_arm = Arm(self.probabilities[i], i)
            self.arms.append(temp_arm)
    
    def get_total_rewards(self):
        '''
        Parameters: self
        Returns: A string listing the number of wins in the current game, the number of 
        losses in the current game, and the reward rate
        '''
        total_wins = 0
        for i in range(self.num_arms):
            total_wins += self.arms[i].number_wins
        string = "Total Wins: " + str(total_wins) + " ; Total Losses: " + str(self.trial - total_wins) + " ; Reward Rate:  " + str(total_wins / self.trial)
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
        
        
class Arm:
    
    def __init__(self, probability, number):
        self.number_wins = 0
        self.number_choices = 0
        self.probability = probability
        self.number = number
    
    def expected(self):
        '''
        Parameters: self
        Returns: the expected value of the arm in question
        '''
        #Avoid divide by zero
        if self.number_choices != 0:
            return self.number_wins / self.number_choices
        else:
            return 0


def pi_first(game):
    '''
    Implements the Pi-First heuristic.
        
    Parameters: 
        game: current game object being played
            
    Returns: a tuple that contains the current trial's choice and result
    '''
    next_choice = decide_next_move(game)
    result = calculate_result(next_choice, game)
    update_game(next_choice, result, game)

    return (next_choice, result)


def decide_next_move(game):
    '''
    Decides which arm to choose next depending on the Pi-First heuristic.

    Parameters: the game object
    
    Returns: an the arm object that will be chosen next
    '''
    random_num = random.random()
    
    if game.trial < game.pi:
        #Explore
        return choose_randomly(game)
        
    else:
        if random_num <= game.gamma:
            #Exploit
            best_arm_value = game.arms[0].expected() 
            arms_with_best_value = []

            #Find the arm with the best expected value
            for i in range(game.num_arms):
                if game.arms[i].expected() > best_arm_value:
                    best_arm_value = game.arms[i].expected()

            #Check if more than one arm has the best expected value
            for i in range(game.num_arms):
                if game.arms[i].expected() == best_arm_value:
                    arms_with_best_value.append(game.arms[i])

            #Choose randomly from the list of arms with the best expected value
            random_num = random.randint(0, len(arms_with_best_value) - 1)

            return arms_with_best_value[random_num]  

        #Fail to exploit; explore (choose randomly)
        else:
            return choose_randomly(game)
            

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
    prob_success = choice.probability
    
    if win_number <= prob_success:
        return 1
    else:
        return 0
    
def update_game(choice, result, game):
    '''
    Updates expected win rates for arms and trial count after each trial
    
    Parameters: 
        choice: last arm object chosen
        result: win or loss (1 or 0)
    '''
    game.trial += 1
    choice.number_choices += 1
    if result == 1:
        choice.number_wins += 1
        
    
def choose_randomly(game):
    '''
    Chooses one arm randomly.
    
    Returns: an arm object
    '''
    randint = random.randint(0, game.num_arms - 1)
    return game.arms[randint]


def run_pi_first_simulation(n, trials, choices_filename, results_filename, num_arms, pi, gamma, environment):
    '''    
    Parameters: 
        n: number of games
        trials: number of trials for each game
        choices_filename: file to be created and written with choice data
        results_filename: file to be created and written with results data
        num_arms: number of arms in the game
        pi: a value for pi
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
        game = Game(num_arms, pi, gamma, environment)
        choices_file.write("\n")
        results_file.write("\n")
        
        #Run trials for each game        
        for j in range(trials):
            trial = pi_first(game)
            choices_file.write(str(trial[0].number))
            results_file.write(str(trial[1]))
            #Write a comma after the result if the trial is not the last trial
            if j < trials - 1:
                choices_file.write(",")
                results_file.write(",")
            
            
def generate_model_data():
    '''
    Run the Pi-First model in neutral, sparse, and plentiful environments with parameters
    chosen for our experiment.
    '''
    #Neutral environment
    run_pi_first_simulation(500, 8, "./ModelData/PiFirst/piFirstNeutral8Choices.csv", "./ModelData/PiFirst/piFirstNeutral8Results.csv", 2, 4, .9, "n")
    run_pi_first_simulation(500, 16, "./ModelData/PiFirst/piFirstNeutral16Choices.csv", "./ModelData/PiFirst/piFirstNeutral16Results.csv", 2, 8, .9, "n")
    
    #Sparse environment
    run_pi_first_simulation(500, 8, "./ModelData/PiFirst/piFirstSparse8Choices.csv", "./ModelData/PiFirst/piFirstSparse8Results.csv", 2, 4, .9, "s")
    run_pi_first_simulation(500, 16, "./ModelData/PiFirst/piFirstSparse16Choices.csv", "./ModelData/PiFirst/piFirstSparse16Results.csv", 2, 8, .9, "s")
    
    #Plentiful environment
    run_pi_first_simulation(500, 8, "./ModelData/PiFirst/piFirstPlentiful8Choices.csv", "./ModelData/PiFirst/piFirstPlentiful8Results.csv", 2, 4, .9, "p")
    run_pi_first_simulation(500, 16, "./ModelData/PiFirst/piFirstPlentiful16Choices.csv", "./ModelData/PiFirst/piFirstPlentiful16Results.csv", 2, 8, .9, "p")
    
#generate_model_data()