# tic-tac-toe
This repository contains a work I have done during for a course I took in my engineering school. The idea was to study different AI approaches using the game Tic-Tac-Toe as an example. Since studying the simple version was, in my opinion, not interesting enough, I decided to push it to the Ultimate Tic-Tac-Toe which is a lot more complex.

## AI implemented
Two main AIs are implemented.  

### Best first
The idea is to use an evaluation function to consider the best next move out of all possible moves. The evaluation function considered is a quadratic function taking the sum of the difference of pieces of the two players squared for each row, column, and diagonal.

### Min Max (+Alpha Beta)
A classic Min Max is implemented. Here the evaluation of a board is the difference between the number of winning states. Thus we only need to consider the
<p align="center"><a href="https://materiaalit.github.io/intro-to-ai/part2/"><img src="https://user-images.githubusercontent.com/26343297/204091104-f7ada11d-dc2c-4c6d-9ec8-f52f80d62aff.png" width="500"></a></p>
The Alpha Beta improvement is also implemented and allows the program to get rid of unnecessary branches.
<p align="center"><a href="https://materiaalit.github.io/intro-to-ai/part2/"><img src="https://user-images.githubusercontent.com/26343297/204090892-d6c568fa-fdae-45a5-bf3e-cbfdecbb23e4.png" width="500"></a></p>

### Monte Carlo Tree Search

This AI has not been implemented yet.

## Ultimate Tic-Tac-Toe
The idea behind this version of the Tic-Tac-Toe is that a move in a sub-board conditions the sub-board where the next moves will be played. For example, playing in the bottom left square of any sub-board will force the next move to be in the bottom left sub-board. Thus, the complexity of the game drasticaly increases. An immediate observation is that the different AIs created for the simple version won't work as well as for the said version. Indeed, now the AI will only try to win the current sub-board and not the whole board. The code in this repository doesn't currently give an improvement to these AIs to fit the ultimate version. However, some improvement ideas are 

<p align="center">
<img src="https://user-images.githubusercontent.com/26343297/204090194-56d42675-10e7-4cd6-92a7-507b9abc2724.png" alt="ultimate-ttt" width="500"/>
</p>

### Possible improvements
I identified two main improvements to make so that an AI can play better:  
  
**First:** We can use an evaluation function that considers other parameters than the current sub-board. For instance, for each move, we can apply an evaluation function to the sub-board it leads to and combine it to the current sub-board evaluation function.

**Second:** We can consider a Monte Carlo Tree Search which wasn't considered for the simple version since it relies on probability and can completely develop the tree of the game thus evading the strategic complexity of the game.
