#from ProgramPP1 import PP1
import pytest
import sys
import importlib

test_values=[
(1,1,2),
(1,5,6),
(1,0,1),
(2,1,3),
]

def test_pp1():
	problem = str(sys.argv[2]).split('.')[0]

	#create a module from the custom Problem file and import it
	my_module = importlib.import_module(problem)

	for v in test_values:
		assert my_module.PP1(v[0],v[1]) == v[2]

