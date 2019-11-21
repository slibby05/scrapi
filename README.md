Steven's CRAppy Prolog Interpreter!

This is a small interpreter to let you play around with SLD resolution

You can run it with 
./scrapi file.pl query

example:
./scrapi file.pl p

where file.pl is
p :- a, b.
a :- c.
a :- d.
b.
d.

Note that this interpreter doesn't support free variables.
