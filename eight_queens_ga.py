import numpy as n
import random
import pandas
import math
import sys
from pandas.io.json import json_normalize as js
from datetime import datetime

start_timestamp=datetime.now() #Start time of the execution
candidate_score={} #Dictionary to maintain population index and score

QUEENS=8 #Number of queens or the board dimension to use
POPULATION=3 #Limit for the initial population
GENESIS=2 #Constant to the set the number of genesis that would crossover
INIT=0 #Default starting point for all counters

ITERATION=INIT #Will be used to count the number of iterations it took
THRESHOLD=1000 #Threshold to limit the number of iterations


def populate(gene, depth):
    """ 
    This function would generate an initial population to find the fittest 
    board configuration.
    
    Parameters
    ---------------------------------------------------------------------------
    gene: int
        defines the dimension of the board
    depth: int
        defines the total number of board configurations to produce for the
        initial population.
    
    Returns
    ---------------------------------------------------------------------------
    list
        provides a list of entire initiation population enemurating board 
        configurations.
    """
    
    boards=[]
    configurations=INIT
    init_candidate=n.arange(gene).tolist()
    while configurations < depth:
        candidate=random.sample(init_candidate, len(init_candidate))
        boards.append(candidate)
        configurations+=1
    return boards

def score(candidates): 
    """ 
    This function would be used to determine the score for each member of the
    population (board configuration).
    
    Lower score indicates better configuration. A score of zero indicates the 
    fittest member.
    
    Parameters
    ---------------------------------------------------------------------------
    candidates: list
        list of population that needs to be scored
        
    Returns
    ---------------------------------------------------------------------------
    dict
        a dictionary where keys represent the index of member 
        population and vaue represent the calculated score
    """
    if all(isinstance(candidate,list) for candidate in candidates):
        for members in candidates:
            resulting_score=INIT
            resulting_score=producescore(members)
            candidate_score[candidates.index(members)]=resulting_score
    else:
        resulting_score=INIT
        resulting_score=producescore(candidates)
        candidate_score[0]=resulting_score
    return candidate_score

def producescore(scoringlist):
    """ 
    This function would calculate the score for a specific board configuration
    
    Lower score indicates better configuration. A score of zero indicates the 
    fittest member.
    
    Score is calculated by identifying if a queen is endangered by another
    queen on the board by looking at the row, column and diagonal positions.
    
    Parameters
    ---------------------------------------------------------------------------
    scoringlist: list
        list representing the board configuration with list index representing 
        the column on the board and list element representing the row where the
        queen is located
        
    Returns
    ---------------------------------------------------------------------------
    int
        calculated score based on the number of endangered positions.
    """
    endangered_score=INIT
    if(len(scoringlist)-len(n.unique(scoringlist))!=0):
        endangered_score+=1
    for row in range(QUEENS):
        for col in range(QUEENS):
            if(row!=col):
                if(abs(scoringlist[row]-scoringlist[col])-abs(row-col)==0):
                    endangered_score+=1
    return endangered_score

def crossmutate(maters, arbitrary=False):
    """ 
    This function would perform cross over and mutation
    
    Cross over will be performed by merging two of the highest configuration
    that had a higher likelihood of producing fittest board configuration.
    
    Mutation is performed by shuffling the positions for the top two 
    configurations.
    
    Parameters
    ---------------------------------------------------------------------------
    maters: list
        list of two members that would undergo crossover and mutation
    
    arbirtary: boolean
        determines if we slice the configurations arbitrailty or split in half.
        Values:
            True: Perform arbitrary slice
            False (Default): Slice in half
        
    Returns
    ---------------------------------------------------------------------------
    list
        Resulting cross over and mutated population.
    """
    crossmutate_kid=[]
    if arbitrary:
        start_split=1
        end_split=QUEENS-2*start_split
        split=random.randint(start_split,end_split)
    else:
        split=math.ceil(QUEENS/2)
    if len(maters)!=2:
        raise CustomError("At least two maters are needed for crossover.")
    else:
        crossmutate_kid.extend(maters[0][:split])
        crossmutate_kid.extend(maters[1][split:])
        crossmutate_kid=[crossmutate_kid]
        crossmutate_kid.append(random.sample(maters[0], len(maters[0])))
        crossmutate_kid.append(random.sample(maters[1], len(maters[1])))
    return crossmutate_kid

def getGenesis(genpopulation, probables):
    """ 
    This function would be used to extract top two genesis for performing cross
    over and mutation from a population that was scored.
    
     
    Parameters
    ---------------------------------------------------------------------------
    probables: list
        ordered list of population. Population is ordered by their score.
    
        
    Returns
    ---------------------------------------------------------------------------
    list
        list of genesis which would undergo cross over and mutation.
    """    
    eligibles=[]
    for seeders in probables[:GENESIS]:
        eligibles.append(genpopulation[seeders])
    return eligibles
    
def fit(COUNTER, FRAME):
    """ 
    Function would help determine if we have find the fittest configuration of
    the board while we have not exhausted the planned iterations.

    Parameters
    ---------------------------------------------------------------------------
    COUNTER: int
        Current iteration number to help determine if we have reached threshold
    FRAME: dataframe
        Dataframe with the score of member population
        
    Returns
    ---------------------------------------------------------------------------
    boolean
        Establish if we have a fit configuration in the population.
        Values:
            True: Yes! We have a configuration that secures all queens.
            False: Not yet! We need to keep hunting for the configuration.
    """     
    if COUNTER < THRESHOLD:
        if not FRAME.empty:
            if FRAME['Score'].iloc[0]==0:
                return True
            else:
                return False
        else:
            return False
    else:
        return True
    
class CustomError(Exception):
    pass

def main():
    ITERATION=INIT
    column_name=['Score'] #Dataframe column header
    scoresheet=pandas.DataFrame(columns=column_name) #Dataframe for discovery of fittest
    crossover_population=[] #List of population resulting from cross over

    probable_candidates=populate(QUEENS, POPULATION)
    scoresheet=js(score(probable_candidates)).T
    scoresheet.columns=column_name
    scoresheet=scoresheet.sort_values(by='Score',ascending=True)     
    
    while not fit(ITERATION, scoresheet):
        """ If the starting population does not have the fittest candidate perform
        cross over and mutation.
        """
        crossover_population=crossmutate(getGenesis(probable_candidates,scoresheet.index.tolist()))
        scoresheet=js(score(crossover_population)).T
        scoresheet.columns=column_name
        scoresheet=scoresheet.sort_values(by='Score',ascending=True)     
        scoresheet.columns=column_name
        ITERATION+=1
    
    fittest=scoresheet.index[scoresheet['Score']==0].tolist()
    
    standard_stdout=sys.stdout
    result="results-from-"+str(datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))+".txt"

    for l in fittest:
        with open(result, 'w') as commitresult:
            sys.stdout=commitresult    
            if ITERATION > 0:
                print("This population needed crossover and mutation")
                print("==================RESULT=====================")
                print(n.asanyarray(crossover_population[l]))
                print("=============================================")
                print("It took "+str(ITERATION)+" iterations to find the fittest!")
                print("Total time taken "+str(datetime.now()-start_timestamp))
                print("Configuration for this result")
                print("-----------------------------")
                print("Queens: "+str(QUEENS))
                print("Initial Population: "+str(POPULATION))
                print("Maximum Iterations allowed: "+str(THRESHOLD))
                print("-----------------------------")
            else:
                print("==================RESULT=====================")
                print(n.asarray(probable_candidates[l]))
                print("=============================================")
                print("It took "+str(ITERATION)+" iterations to find the fittest!")
                print("Total time taken "+str(datetime.now()-start_timestamp))
                print("Configuration for this result")
                print("-----------------------------")
                print("Queens: "+str(QUEENS))
                print("Initial Population: "+str(POPULATION))
                print("Maximum Iterations allowed: "+str(THRESHOLD))
                print("-----------------------------")
            sys.stdout=standard_stdout 

if __name__=="__main__":
    main()