# Hoot Owl Hoot (recommended to view in a Markdown editor)
This is my CPSC 474 final project for the game Hoot Owl Hoot. More details can be found in the video "BThomas_HootOwlHoot" on Canvas Media Library. For this project, I decided to explore different strategies surrounding the game by constructing 5 different agents to determine which are most and least effective as well as to analyze how the game's unique properties interact with the agents. Running "make" will create the 4 executables and run a small test suite.

Research Question: **In the game Hoot Owl Hoot, how much better can an agent utilizing backwards induction via dynamic programming perform compared to four other agents utilizing rule-based, greedy, and MCTS strategies?** 

## Game Description
Hoot Owl Hoot is a game consisting of a board with two different tracks: a color track and a sun track. Owls move on the color track whereas the sun moves on the sun track. Players are given 3 cards of either colors or a sun and choose one of their cards each turn to move an owl of their choice to the next open space of that color on the board. If a player has a sun card, they are required to play it and advance the sun track. The goal of all players is to work together to move all owls (of which there are 3-6 depending on player preference) to the end of the track (the nest) before the sun reaches the end of its track. Hoot Owl Hoot is a **stochastic, perfect information, turn-based, and acyclic game.**

## Code
 **dp_agent.py** contains the code for the DP agent which uses backwards induction to determine the values of states. It does so using top-down recursion with memoization. I set up some basic variables to help represent the game (board, cards, card_probabilities) and a helper function to determine terminal states. I then recurse through states to determine the values of states. In doing so, I consider all possible cards and all possible owls we could move to arrive at an overall probability. I additionally have functionality to determine the best action to take given a set of cards via command-line argument similar to Shut the Box as well as functionality to run. I also have functionality to run a certain number of games with a certain starting state, where I add some variance by introducing random cards. Program can be ran using **./DP**

 **greedy_agent.py** contains the code for the greedy agent, which utilizes a strategy of always making whichever move would result in the most forward progress without consideration for future states. It reuses much of the same code for the DP agent and can be ran using **./Greedy**

**rulebased_agent.py** contains the code for two rule-based agents, which utilize a strategy of either moving the owl furthest from the nest or moving the owl closest to the nest respectively. It randomly picks a card from the set to play and utilizes much of the same code as the DP agent. Can be ran using **./RuleBased**

**mcts_agent.py** contains the code for the agent utilizing MCTS. General strategy was based on Problem Set 4 and utilizes the UCB formula. The code runs MCTS for as many iterations as the user enters and then uses the information it develops in order to select the best move from the state entered. Can be ran using **./MCTS**
## Changes
Note that I have made two rather significant changes to my approach from my video, one of which was that I used top-down dynamic programming with memoization rather than bottom-up dynamic programming as I had intended for my DP agent. I still implemented value iteration in the same manner and would theoretically get the same result. Although I wanted to use the bottom-up approach for more of a twist on the idea, it turned out to be quite difficult to sort states effectively so that we don't reach a state that we haven't been to yet. I presume this is reasonably possible but perhaps out of scope of the expected time to spend on the project as well as secondary to the main idea at hand.

Another significant change I made was adding an MCTS agent because I was very interested to see how it would perform after working on the other agents and becoming more familiar with Hoot Owl Hoot's unique attributes.

I attempted to replicate the game as much as possible. I used a real game board in order to simulate the board and its arrangement of colors as well as the number of color tiles and sun tiles. You can find an example here: https://cdn.montessoriservices.com/product/1200/y712_f13_p.jpg

This represents a change from my simplifications where I had estimated that the branching factor and state space may require me to limit the number of tiles a bit. However, this turned out to be mostly a nonissue. The main simplification for my version of Hoot Owl Hoot is a uniform probability distribution. Since Hoot Owl Hoot uses a deck of cards rather than a dice roll as in Shut the Box, the probability of getting certain cards changes over the course of the game. This doesn't seem like something well fit for backwards induction to handle, but attempting to implement this would be a great goal for extending the project. 

## Running the Agents
There are multiple ways to run the executables based on command-line arguments to access different features, and the executables share many of the same ways. Run the executable you want to test with no arguments to see all the possible configurations, or you can alternatively see the execution of the tests.

A state is represented as integers separated by commas where the last integer represents the sun position and the rest are owl positions. An example is as follows: 

    5,4,3,0

This represents the starting position for 3 owls and indicates owl 1 at index 5 on the board, owl 2 at index 4, and owl 3 at index 3 with the sun at the first index. 0 to 39 are the valid indexes for owls and 0 to 13 are the valid indexes for the sun. You can use up to 6 owls but runtime may slow down dramatically, particularly for the DP agent.

Cards are represented as three valid card colors with commas between them and no spaces. There are 7 valid cards: red, green, blue, purple, yellow, orange, and sun. Example:

    red,green,purple

For the rule-based agent, you will need to specify "front" or "back" in the last command-line argument to determine whether to use the agent that always moves the owl closest to the nest or the owl furthest from the nest respectively.

## Evaluation
I've chosen to evaluate my DP agent in comparison to four other agents, two of which are rule-based, one of which is MCTS, and one of which is greedy. One agent always moves the owl closest to the nest, one agent always moves the owl furthest from the nest, and the final agent selects the owl which would gain the largest progress from the move. All evaluation is performed with only three owls for the sake of time over the course of many games. For each agent except MCTS, we start at the initial position for 3 owls and pick the best card out of our set, then pick a new random card to replace it and keep going until we get a terminal state. We then evaluate whether we won or loss and then start a new game and keep going. For MCTS, I took a different approach, running the program several times with various numbers of iterations to determine how often it took the same move as the DP agent. 

## Observations and Takeaways

Here are some findings I believe to be noteworthy:
 - Increasing the number of owls decreases the chance of winning with the DP agent. In a set up where all games start from the starting position, 3 owls produced a 92% chance of winning whereas 4 owls produced a 84% chance of winning. These results highlight how, even with optimal play, random chance plays an increasingly large factor as you add more owls. 
 - As expected, value iteration performed very similar to whatever the calculated value of the state was.
 - The two rule-based agents performed very differently from one another, namely the front agent in particularly averaged around a 50% win rate from the starting state with 3 owls while the back agent had results around 86%, just slightly below the DP agent. This also aligns quite well with the greedy agent as, typically, we'd expect the owl furthest back to be able to make the most progress. This difference also demonstrates that the owl you move is likely more important than the card you choose given that random cards were selected for each rule-based agent to play.
 - The DP agent and greedy agent performed very similarly with 3 owls, with the DP agent only being marginally better. However, in nearly all cases, the DP agent did appear to barely edge out the greedy agent by just a few percent. This means that there isn't much in the way of future rewards that we have to consider in Hoot Owl Hoot, but there is still a consistent and notable difference.  
 - The branching factor, as I predicted, was perhaps the most significant piece of the problem and had a huge effect on runtimes for the DP agent. From the starting position, 3 owls takes only a few seconds while 4 owls takes a few minutes. Increasing the number of owls added multiple new possible moves and many, many new states. In an extension of this project where I try to optimize the AI completely, I might consider an implementation that runs value iteration for 3 to 4 owls and MCTS for 5 to 6 owls, which is better equipped to handle the scale of the branching factor.
 - The MCTS agent with 10000 iterations often chose the same action as the DP agent when running from the initial position for 3 owls and with the same card configuration, although it was not entirely consistent (around 50% of the time). This likely suggests that many of the next states are roughly equal in value to MCTS (and indeed, when analyzing the value of the alternate actions that MCTS chose with the DP agent, they were very close, often just ten-thousandths lower in value compared to the action the DP agent chose).
 - As expected, MCTS has the advantage of much faster runtime compared to the DP agent, particularly relevant with more owls. This makes it a fantastic choice for gaining at least a decent idea of what a best action may be without having to run for hours and hours.
 
## Research Question and Final Results
My research question I posed was: **In the game Hoot Owl Hoot, how much better can an agent utilizing backwards induction via dynamic programming perform compared to four other agents utilizing rule-based, greedy, and MCTS strategies?** 

To answer my question, the DP agent performs just marginally better than the greedy agent with around a 1-3% difference in win probability. However, it runs slightly better against the rule-based agent that selects the owl always furthest from the nest, with around 10-11% difference, and runs substantially better than the rule-based agent that selects the owl always closest to the nest, where we see a 40-45% difference. These results can be seen in the comparison tests provided in my makefile and further testing is welcome.

Furthermore, the MCTS agent often selects moves that are either the same as the DP agent or very similar in value according to the DP agent, reinforcing the effectiveness of the DP agent in selecting worthwhile moves.