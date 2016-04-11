#from ProgramPP2 import PP2
import pytest
import sys
import importlib

test_values=[
(1,1,1),
(2,5,10),
(1,0,0),
(2,2,4),
]

def test_pp1():
	problem = str(sys.argv[2]).split('.')[0]

	#create a module from the custom Problem file and import it
	my_module = importlib.import_module(problem)
	
	for v in test_values:
		assert my_module.PP2(v[0],v[1]) == v[2]

