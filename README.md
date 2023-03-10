# wOBA calculator
This program will calculate wOBA based on a league's stats over an entire season. Certain notation and assumptions will need to be used.
## Game States
- There are twenty-four unique game states in baseball based on the runners on base and the number of outs (eg. runner on first with one out)
- In this program, game states are represented with an ordered pair of a base state (eg. runner on first) and the number of outs
- The base states are represented by the following lowercase letters

    - "a": nobody on  
    - "b": runner on first
    - "c": runner on second
    - "d": runner on third
    - "e": runners on first and second
    - "f": runners on first and third
    - "g": runners on second and third
    - "h": bases loaded

## Events
- In this program, events will be represented with the following capital letters

    - "W": Walk - includes walks and hit by pitches
    - "S": Single
    - "D": Double
    - "T": Triple
    - "H": Home Run
    - "O": Out
    - "P": Productive out - this out is assumed to score a runner if the runner is on third with less than two outs. In all other cases, it is the same as a normal out
- For the purposes of this program, no other events will be considered

## Assumptions
- Assumptions need to be made as to how runners will move from each base on each event
- The following assumptions are used in this program

    - A single will always score a runner from second
    - A double will always score a runner from first
    - A productive out with less than two outs will score a runner from third
    - A productive out in all other situations will not advance runners
    - All regular outs will not advance runners
    - In all other situations, an event will advance the runner as many bases as the batter advances


## Functions of Interest
### search.py
- get_run_expectancy takes in a problem class and returns the run expectancy for the remainder of that inning
- get_probabilities takes in a problem and returns the relative probabilities of being in a certain game state. The total probability for all game states adds up to one

### re24.py
Running this file returns the run expectancy matrix for MLB from 2010-2015
- get_re24_matrix returns a dictionary of all 24 game states and their run expectancies
- get_run_scoring_environment returns an ordered pair of a re24 matrix and the probabilities of being in each of the 24 game states

### linear-weights-constants.py
Running this file outputs fangraphs linear weights constants from the 2015 MLB season and my algorithms constants from that season. It also outputs my calculation of Mike Trout and Martin Maldonado's runs above average from that season. Finally, it outputs the linear weights constants and two players runs above average from the 2022 Rock River League season.
- get_linear_weights_constants takes in a minimum probability and a dictionary with the probability of each event and returns a dictionary of linear weights constants
- calculate_raa takes in a dictionary of linear weights and a player's stats dictionary and returns that players runs above average