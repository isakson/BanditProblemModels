'''
Computational Models of Cognition
Final Project
11/14/18

Functions for implementing and running the Tau-Switch model in a replication study 
of Lee et al. (2011).
'''
import random
import numpy as np

class Game:
    
    def __init__(self, num_arms, tau, gamma, environment):
        self.trial = 0
        self.arms = []
        self.num_arms = num_arms
        self.tau = tau
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
        
        #Determine the environment and sample from the corresponding Beta functions
        for i in range(self.num_arms):
            if environment == "n":
                probabilities.append(np.random.beta(1,1))
            elif environment == "s":
                probabilities.append(np.random.beta(2,4))
            else:
                probabilities.append(np.random.beta(4,2))
                
        return probabilities
    
    def get_state(self):
        '''
        Parameters: self
        Returns: Identifies the state of the current trial and returns "s" if the current trial is in 
        the "same" state, "b" if the current trial is in the "better/worse" state, or "e" if the 
        current trial is in the "explore/exploit" state
        '''
        #An array containing tuples of the number of wins and losses for every arm
        arm_states = []
        for i in range(self.num_arms):
            arm_states.append((self.arms[i].number_wins, self.arms[i].number_losses))
         
        #Booleans containing possible latent states for this trial
        all_same = True
        found_best = False
        explore_exploit = False
        
        first_arm = arm_states[0]
        best_arm = arm_states[0]
        
        #Determine state for this trial
  
        #Find the best arm
        for i in range(len(arm_states)):
            #Check for same case:
            if arm_states[i] != first_arm:
                all_same = False
            #Check for better/worse case:
            if self.is_better(best_arm, arm_states[i]) == -1:
                best_arm = arm_states[i]
        
        #Compare the best arm to the other arms to see if a different arm has more 
        #losses and more wins, in which case we are in an explore/exploit state
        for i in range(len(arm_states)):
            if self.is_better(best_arm, arm_states[i]) == None:
                explore_exploit = True
                
        #If we found no arm with more losses and more wins, we confirmed that the 
        #best arm(s) is strictly better than all others
        if explore_exploit == False:
            found_best = True
        
        #Return the state based on the booleans
        if all_same:
            return "s"
        elif found_best:
            return "b"
        elif explore_exploit:
            return "e"
    
    def get_best_arm(self):
        '''
        Parameters: self
        Returns: A list of arm objects tied for best wins/loss counts; empty list if there are none
        '''
        #Initialize an array containing tuples of the number of wins and losses for every arm
        arm_states = []
        for i in range(self.num_arms):
            arm_states.append((self.arms[i].number_wins, self.arms[i].number_losses))
            
        #Find best arm tuple (note: there may be multiple that match its counts of wins and losses)
        best_arm = arm_states[0]
        for i in range(len(arm_states)):
            if self.is_better(best_arm, arm_states[i]) == -1:
                best_arm = arm_states[i]
        
        #Identify all arm tuples that are tied for best and append their corresponding 
        #arms to best_arm_list
        best_arm_list = []
        for i in range(len(arm_states)):
            if arm_states[i] == best_arm:
                #Append corresponding arm object
                best_arm_list.append(self.arms[i])
        
        return best_arm_list
    
    
    def is_better(self, arm1, arm2):
        '''
        Parameters: 
            self
            arm1 and arm2: two arm tuples (wins,losses) to compare 
        Returns: -1 if arm1 is strictly worse than arm2, 0 if the arms are the same, 1 if arm1
        is strictly better than arm2, and None if neither arm is strictly better (explore/exploit
        scenario)
        '''
        #Case: more successes and fewer failures:
        if arm1[0] > arm2[0] and arm1[1] < arm2[1]:
            return 1
        elif arm2[0] > arm1[0] and arm2[1] < arm1[1]:
            return -1
        #Case: more successes and equal failures:
        elif arm1[0] > arm2[0] and arm1[1] == arm2[1]:
            return 1
        elif arm2[0] > arm1[0] and arm2[1] == arm1[1]:
            return -1
        #Case: equal successes and fewer failures:
        elif arm1[0] == arm2[0] and arm1[1] < arm2[1]:
            return 1
        elif arm2[0] == arm1[0] and arm2[1] < arm1[1]:
            return -1
        #Case: same successes and same failures
        elif arm1[0] == arm2[0] and arm1[1] == arm2[1]:
            return 0
        else:
            return None
        
class Arm:
    
    def __init__(self, probability, number):
        self.number_wins = 0
        self.number_losses = 0
        self.number_choices = 0
        self.probability = probability
        self.number = number
        
        
def tau_switch(game):
    '''
    Implements tau_switch heuristic.
        
    Parameters: 
        game: current game object being played
            
    Returns: a tuple containing this trial's choice and result
    '''
    next_choice = decide_next_move(game)
    result = calculate_result(next_choice, game)
    update_game(next_choice, result, game)
    
    return (next_choice, result)

def decide_next_move(game):
    '''
    Decides which arm to choose next depending on the tau_switch heuristic.

    Parameters: the game object
    Returns: an the arm object that will be chosen next
    '''
    #Identify the state of the game for the current trial
    state = game.get_state()
    
    #Choose the next arm based on state
    
    #Generate a random number to compare to gamma in each state
    gamma_threshold = random.random()
    #Same state: choose randomly
    if state == "s":
        return choose_randomly(game)
    
    #Better/worse state: choose best arm with probability gamma 
    elif state == "b":
        best_arms = game.get_best_arm()
        if gamma_threshold <= game.gamma:
            if len(best_arms) == 1:
                return best_arms[0]
            else:
                #If two or more arms are tied for best, choose randomly among them
                randint = random.randint(0, len(best_arms)-1)
                return best_arms[randint]
        else:
            #Choose randomly among the worse arms
            worse_arms = [x for x in game.arms if x not in best_arms]
            randint = random.randint(0, len(worse_arms) - 1)
            return worse_arms[randint]
    
    #Explore/exploit state:
    else:
        most_explored_arm = game.arms[0]
        for i in range(len(game.arms)):
            if game.arms[i].number_choices > most_explored_arm.number_choices:
                most_explored_arm = game.arms[i]
        most_explored_list = [most_explored_arm]

        #Determine explore or exploit
        if (gamma_threshold <= game.gamma and game.trial <= game.tau) or (gamma_threshold > game.gamma and game.trial > game.tau):
            #Explore: choose the alternative that is NOT the most explored
            #Note: we're going to choose any arm that has NOT been chosen the most
            less_explored_arms = [x for x in game.arms if x not in most_explored_list]
            randint = random.randint(0, len(less_explored_arms)-1)
            return less_explored_arms[randint]   
        else:
            #Exploit: choose the alternative that IS the most explored
            #Note: we're going to choose the arm that has been chosen the most
            return most_explored_arm

        
def calculate_result(choice, game):
    '''
    Calculates the outcome of the choice (a win or a loss) based on the probabilities associated with each arm

    Parameters: 
        choice: the choice of arm (0 or 1)
        game: the game object being played, which holds the probabilities of success for the arms

    Returns: int outcome
    '''
    win_number = random.random()   
    #Probability of success for the chosen arm
    prob_success = choice.probability
    
    #Determine win or loss
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
    
    #Increment the number of choices for the arm that was chosen
    choice.number_choices += 1
    
    #Increment the win/loss count for the arm that was chosen
    if result == 1:
        choice.number_wins += 1
    else:
        choice.number_losses += 1
        
        
def choose_randomly(game):
    '''
    Chooses one arm randomly.
    
    Returns: an arm object
    '''
    randint = random.randint(0, game.num_arms - 1)
    return game.arms[randint]


def run_tau_switch_simulation(n, trials, choices_filename, results_filename, num_arms, tau, gamma, environment):
    '''
    Parameters: 
        n: number of games
        trials: number of trials for each game
        choices_filename: file to be created and written with choice data
        results_filename: file to be created and written with results data
        num_arms: number of arms in the game
        tau: a value for tau
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
        game = Game(num_arms, tau, gamma, environment)
        choices_file.write("\n")
        results_file.write("\n")
        
        #Run trials for each game
        for j in range(trials):
            trial = tau_switch(game)
            choices_file.write(str(trial[0].number))
            results_file.write(str(trial[1]))
            #Write a comma after the result if the trial is not the last trial
            if j < trials - 1:
                choices_file.write(",")
                results_file.write(",")
                
def generate_model_data():
    '''
    Run the Tau-Switch model in neutral, sparse, and plentiful environments with parameters 
    chosen for our experiment.
    '''
    #Neutral environment
    run_tau_switch_simulation(500, 8, "./ModelData/TauSwitch/tauSwitchNeutral8Choices.csv", "./ModelData/TauSwitch/tauSwitchNeutral8Results.csv", 2, 4, .9, "n")
    run_tau_switch_simulation(500, 16, "./ModelData/TauSwitch/tauSwitchNeutral16Choices.csv", "./ModelData/TauSwitch/tauSwitchNeutral16Results.csv", 2, 8, .9, "n")
    
    #Sparse environment
    run_tau_switch_simulation(500, 8, "./ModelData/TauSwitch/tauSwitchSparse8Choices.csv", "./ModelData/TauSwitch/tauSwitchSparse8Results.csv", 2, 4, .9, "s")
    run_tau_switch_simulation(500, 16, "./ModelData/TauSwitch/tauSwitchSparse16Choices.csv", "./ModelData/TauSwitch/tauSwitchSparse16Results.csv", 2, 8, .9, "s")
    
    #Plentiful environment
    run_tau_switch_simulation(500, 8, "./ModelData/TauSwitch/tauSwitchPlentiful8Choices.csv", "./ModelData/TauSwitch/tauSwitchPlentiful8Results.csv", 2, 4, .9, "p")
    run_tau_switch_simulation(500, 16, "./ModelData/TauSwitch/tauSwitchPlentiful16Choices.csv", "./ModelData/TauSwitch/tauSwitchPlentiful16Results.csv", 2, 8, .9, "p")
    
#generate_model_data()