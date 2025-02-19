all: DP Greedy RuleBased MCTS start tests

DP:
	echo "#!/bin/bash" > DP
	echo "python3 dp_agent.py \"\$$@\"" >> DP
	chmod u+x DP

Greedy:
	echo "#!/bin/bash" > Greedy
	echo "python3 greedy_agent.py \"\$$@\"" >> Greedy
	chmod u+x Greedy

RuleBased:
	echo "#!/bin/bash" > RuleBased
	echo "python3 rulebased_agent.py \"\$$@\"" >> RuleBased
	chmod u+x RuleBased

MCTS:
	echo "#!/bin/bash" > MCTS
	echo "python3 mcts_agent.py \"\$$@\"" >> MCTS
	chmod u+x MCTS


start: 
	$(info Welcome to Hoot Owl Hoot! Run "make tests" to run tests and see example program execution. Run any of the 4 executables (DP, Greedy, RuleBased, MCTS) with no arguments to view usage instructions, and see TEST_SCRIPT.md for more information.)
	   $(info ************  STARTING TESTS ************)

DP_tests:
	$(info ************  DP TESTS ************)
	./DP 5,4,3,0
	./DP 5,4,3,0 10000
	./DP 5,4,3,0 red,green,yellow
	./DP 10,19,6,5
	./DP 28,25,23,10 orange,purple,blue

Greedy_tests:
	$(info ************  GREEDY TESTS ************)
	./Greedy 5,4,3,0 100000
	./Greedy 5,4,3,2,0 100000
	./Greedy 16,29,35,11 red,yellow,blue
	./Greedy 28,31,9,14,7 orange,purple,blue
	./Greedy 39,39,39,9,12 1000

RuleBased_tests:
	$(info ************  RULEBASED TESTS ************)
	./RuleBased 5,4,3,0 1000 front
	./RuleBased 5,4,3,0 1000 back
	./RuleBased 19,12,28,3 red,yellow,blue front
	./RuleBased 39,39,12,1 orange,purple,green back
	./RuleBased 5,4,3,2,1,0 10000 back

MCTS_tests:
	$(info ************  MCTS TESTS ************)
	./MCTS 5,4,3,0 1000 red,green,yellow
	./MCTS 10,19,6,5 1000 orange,purple,blue
	./MCTS 28,25,23,10 1000 blue,purple,red
	./MCTS 5,4,3,2,1,0 1000 green,red,blue
	./MCTS 5,4,3,2,0 10000 purple,yellow,orange

compare_tests:
	$(info ************  BASIC COMPARISON TESTS ************)
	./DP 5,4,3,0 10000
	./Greedy 5,4,3,0 10000
	./RuleBased 5,4,3,0 10000 front
	./RuleBased 5,4,3,0 10000 back
	./DP 19,12,28,3 red,yellow,blue
	./Greedy 19,12,28,3 red,yellow,blue
	./RuleBased 19,12,28,3 red,yellow,blue front
	./RuleBased 19,12,28,3 red,yellow,blue back
	./DP 39,39,12,1 10000
	./Greedy 39,39,12,1 10000
	./RuleBased 39,39,12,1 10000 front
	./RuleBased 39,39,12,1 10000 back
	./DP 19,12,28,3,10 10000
	./Greedy 19,12,28,3,10 10000
	./RuleBased 19,12,28,3,10 10000 front
	./RuleBased 19,12,28,3,10 10000 back
	./DP 5,4,3,0 red,green,yellow
	./MCTS 5,4,3,0 10000 red,green,yellow
	./DP 10,19,6,5 orange,purple,blue
	./MCTS 10,19,6,5 10000 orange,purple,blue
	./DP 28,25,23,10 blue,purple,red
	./MCTS 28,25,23,10 10000 blue,purple,red

long_tests:
	$(info ************  LONGER TESTS *feel free to terminate early* ************)
	./DP 5,4,3,2,0
	./MCTS 5,4,3,2,0 1000000 orange,blue,purple
	./DP 5,4,3,2,1,0


tests: DP_tests Greedy_tests RuleBased_tests MCTS_tests compare_tests long_tests


clean: 
	rm -f DP Greedy RuleBased MCTS