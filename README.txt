Computational Models of Congition
Final Project
11/13/2018

This folder contiains:

1. Five Python files with code for the five heuristic models and data analysis 
     - win_stay_lose_shift.py contains functions implementing Win-stay, lose-shift
     - epsilon_heuristics.py contains functions implementing Epsilon-greedy and Epsilon-decreasing
     - pi_first.py contains functions implementing Pi-First
     - tau_switch.py contains functions implementing Tau-Switch
     - data_analysis.py contains functions analyzing our data and Lee et al.'s (2011) data.
     
2. The directory LeeCSV, which contains participant data from Lee et al. (2011) which we exported 
from MatLab into CSV form. (The files are labeled with the first and last initial of the participant, 
the number of trials, and the alpha and beta parameters for the Beta distribution corresponding to 
condition. For instance, participant AH playing 8-trial games in the neutral environment [With arm 
probabilities generated with Beta(1,1)] corresponds to the file ah-8-S_A1-B1_dat.matchoices.csv.)
    Within LeeCSV, there are two directories:
    - The Choices directory, which contains data from each participant on which arm they chose for
    each trial of each game.
    - The Results directory contains data from each participant on which whether the arm they chose 
    won or lost for each trial of each game.
    
3. The directory ModelData, which contains directories for each model, with .csv data corresponding 
to each condition. The ModelData directory also contains the directory ModelAverages, which contains 
the text files with our analysis of the models' performances. 

4. The .txt files averages.txt and choices_data.txt, which contain analysis of the Lee et al. (2011) 
data. choices_data.txt includes the data for each participant, and averages.txt contains the data 
averaged across all 10 of Lee et al.'s (2011) participants.

5. The directory 6ArmData, which contains directories for each model, with .csv data. The 6ArmData directory also contains the directory Averages, which contains the text file with our analysis of the 
models' performances.

6. FigureGenerationAndDataExtractionCode.ipynb, which is a Jupyter notebook containing the code we used to generate our graphs and do our data handling.

7. FigureGenerationAndDataExtractionCode.html, which contains the above Jupyter notebook, exported as an .html file.

8. FinalProjectPaper.pdf, our final project paper.


Running files:

- Models:
    We have commented out the last line on each of the model files, so running them should not 
    generate new data, but if you wanted to generate new data, you could uncomment the last line in 
    any/all of the models and run them from the command line (e.g. python3 tau_switch.py). If you do 
    this, the CSV data in the ModelData directory (and its subdirectories) will be replaced with new 
    data produced by the models.
    
- data_analysis.py:
    Three function calls are commented out at the bottom of data_analysis.py. 
    1. analyze_all_models() will analyze whatever data is in the sub-directories within the 
    directory ModelData, and write the results to the text files in the ModelAverages directory 
    within ModelData.
    2. analyze_Lee_data() will analyze the data in the directory LeeCSV and write the 
    results to the files averages.txt and choices_data.txt. Unless the LeeCSV data files have been 
    changed, running this function should not change what is written to the two text files.
    3. proof_of_concept_6_arm_problems() generates and analyzes data for all 5 heuristics with
    500 50-trial 6-arm games in a neutral environment. If uncommented and run, the function will overwrite the data in the 6ArmData directory.