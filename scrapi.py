from Goal import(Goal, choice)
from Parser import(parse)
from Exceptions import(LexException, ParseException)
from sys import argv
from copy import deepcopy

def main():
    # try to parse the program
    # if I fail, give up and die
    try:
        program = parse(open(argv[1], 'r').read())
        query = argv[2]
    except (LexException, ParseException) as e:
        print(e)
        return

    # Print out the program
    print("Program:")
    for (p,clauses) in program.items():
        for clause in clauses:
            if len(clause) == 0:
                print(p + ".")
            else:
                print(p + " :- " + ", ".join(clause) + ".")
    print("\n")
    goalStack = [Goal(query)]

    while len(goalStack) != 0:

        print("GS = " + ",".join([str(g) for g in goalStack]) + ".")

        # get the current goal
        goal = goalStack.pop(0)

        # If the goal is a choice, then our goal stack looks like
        # ?<[a,b], [c,d]>, e ...
        # We want to remove the first option
        # and put that on the goal stack
        # so It should look like
        # a,b, ?<[c,d]>, e ...
        #
        # If the choice becomes empty, we discard it
        # ?<[a,b]>, d, e ..
        # becomes
        # a, b, d, e ..
        # instead of 
        # a, b, ?<>, d, e ..
        if goal.choice():
            firstChoice = goal.first()
            if not goal.empty():
                goalStack.insert(0,goal)
            for g in reversed(firstChoice):
                goalStack.insert(0,Goal(g))

        else:
            # if the current goal isn't a choice, then
            # 1. look it up in the program
            # 2. if the rule isn't a parallel rule, 
            #    Add all goals to the goal stack
            # example:
            # GS = p,x,y
            # p :- a,b,c
            # then
            # GS = a,b,c,x,y
            # 3. if the rule parallel rule, 
            #    Then add a new choice to the goal stack
            # GS = p,x,y
            # p :- a,b,c
            # p :- d,e,f
            # then
            # GS = ?<[a,b,c], [d,e,f]>, x, y
            if goal.var() in program:
                newGoals = deepcopy(program[goal.var()])
                if len(newGoals) == 1:
                    for g in reversed(newGoals[0]):
                        goalStack.insert(0, Goal(g))
                else:
                    goalStack.insert(0, choice(newGoals))

            # the current goal isn't in the program
            # That means it's a failure, so backtrack to the last choice.
            #
            # example:
            # GS = d,e,f ?<[a,b,c]>, x, y
            # d not defined
            # GS = ?<[a,b,c]>, x, y
            else:
                print("BACKTRACKING " + goal.var(), end=" ")
                while not goalStack[0].choice():
                    print(goalStack.pop(0), end=" ")
                print()

if __name__ == "__main__":
    main()
