import random
import numpy as np
import sys
from domain.make_env import make_env
from domain.task_gym import GymTask
from neat_src import *


class WannGymTask(GymTask):
  """Problem domain to be solved by neural network. Uses OpenAI Gym patterns.
  """ 
  def __init__(self, game, paramOnly=False, nReps=1): 
    """Initializes task environment
  
    Args:
      game - (string) - dict key of task to be solved (see domain/config.py)
  
    Optional:
      paramOnly - (bool)  - only load parameters instead of launching task?
      nReps     - (nReps) - number of trials to get average fitness
    """

    GymTask.__init__(self, game, paramOnly, nReps)
    #print(game, "gaaaaame")


# -- 'Weight Agnostic Network' evaluation -------------------------------- -- #
  def setWeights(self, wVec, wVal, isRandom=False):
    """Set single shared weight of network

    #wVals = [0.5,1.0,2.0]
    #isRandomDist = [True, False]  ######################################


    Args:
      wVec    - (np_array) - weight matrix as a flattened vector
                [N**2 X 1]
      wVal    - (float)    - value to assign to all weights
  
    Returns:
      wMat    - (np_array) - weight matrix with single shared weight
                [N X N]
    """
    # Create connection matrix
    wVec[np.isnan(wVec)] = 0
    dim = int(np.sqrt(np.shape(wVec)[0]))    
    cMat = np.reshape(wVec,(dim,dim))
    cMat[cMat!=0] = 1.0
  

###############################################################
    #for iVal in range(wVals):
     # for isRandom in isRandomDist:
      #  wMat = self.setWeights(wVal[iVal],wVal,isRandom)

	if isRandom:
	  wVal = np.random.normal(loc=wVal, scale=wVal*0.5, size=cMat.shape)
	  wVal[wVal < 0] = 0.0
	  #s = np.random.normal(mu, sigma, 1000)
	  
    # Assign value to all weights
    wMat = np.copy(cMat) * wVal 
    return wMat


  def getFitness(self, wVec, aVec, hyp, \
                    seed=-1,nRep=False,nVals=6,view=False,returnVals=False):
    """Get fitness of a single individual with distribution of weights
  
    Args:
      wVec    - (np_array) - weight matrix as a flattened vector
                [N**2 X 1]
      aVec    - (np_array) - activation function of each node 
                [N X 1]    - stored as ints (see applyAct in ann.py)
      hyp     - (dict)     - hyperparameters
        ['alg_wDist']        - weight distribution  [standard;fixed;linspace]
        ['alg_absWCap']      - absolute value of highest weight for linspace
  
    Optional:
      seed    - (int)      - starting random seed for trials
      nReps   - (int)      - number of trials to get average fitness
      nVals   - (int)      - number of weight values to test

  
    Returns:
      fitness - (float)    - mean reward over all trials
    """
    if nRep is False:
      nRep = hyp['alg_nReps']

    # Set weight values to test WANN with ######################################################
    if (hyp['alg_wDist'] == "standard") and nVals==6: # Double, constant, and half signal 
      wVals = np.array((0.5,1.0,2.0,0.5,1.0,2.0))
      #wVals2 = np.array((0,0.4,0.8,1.2,1.6,2))
      #wVals3 = np.array((0.5,1.0,2.0))
    else:
      wVals = np.array((0.5,1.0,2.0,0.5,1.0,2.0))
      #wVals = np.linspace(-self.absWCap, self.absWCap ,nVals)


    # Get reward from 'reps' rollouts -- test population on same seeds
    reward = np.empty((nRep,nVals))
    #reward = np.empty((nRep,nVals*2))
    isRandomDist = [False, True]
    #print(isRandomDist,"randDist")
    for iRep in range(nRep):
      #for isRandom in isRandomDist:
      for iVal in range(nVals):
        #for isRandom in isRandomDist:
        #wMat = self.setWeights(wVec,wVals[iVal],isRandom)
        wMat = self.setWeights(wVec,wVals[iVal],isRandom=(iVal>2))
        #wMat = self.setWeights(wVec,wVals[iVal])
        if seed == -1:
          #reward[iRep,iVal + int(isRandom)*nVals] = self.testInd(wMat, aVec, seed=seed,view=view)
          reward[iRep,iVal] = self.testInd(wMat, aVec, seed=seed,view=view)
        else:
          reward[iRep,iVal] = self.testInd(wMat, aVec, seed=seed+iRep,view=view)
          #reward[iRep,iVal] = self.testInd(wMat, aVec, seed=seed+iRep,view=view)
          
    if returnVals is True:
      return np.mean(reward,axis=0), wVals
    return np.mean(reward,axis=0)
 

