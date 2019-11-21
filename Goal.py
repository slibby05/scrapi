

# A goal is a list of choices.
# Wow, that'd sound poetic if it wasn't so dumb.
#
# Anyway, since a choice might contain many new goals,
# a choice is a list of atoms.
# q :- a,b,c.
# q :- d,e,f.
# would be the goal
# [[a,b,c],[d,e,f]]
class Goal():

    def __init__(self, choices, isChoice=False):
        self.isChoice = isChoice
        if isChoice:
            self.choices = choices
        else:
            self.choices = [[choices]]

    # This is a choice goal if we have more than one choice
    def choice(self):
        return self.isChoice

    # If this isn't a choice goal, 
    # then the var is the first thing in the first choice.
    def var(self):
        return self.choices[0][0]

    # if this is a choice goal,
    # then we can get the first choice by poping it from the list
    def first(self):
        return self.choices.pop(0)

    def empty(self):
        return len(self.choices) == 0

    def __str__(self):
        if self.choice():
            def cstr(choice):
                return "[" + ",".join([str(x) for x in choice]) + "]"
            return "?<" + ",".join([cstr(c) for c in self.choices]) + ">"
        else:
            return self.choices[0][0]

#construct a choice goal.
def choice(choices):
    return Goal(choices, True)
