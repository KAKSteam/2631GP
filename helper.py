#!/usr/bin/env python
#Helper Methods

#import load method and treelib
from loader import load

def loadTree(path):
	
	return load(path)

def there_is(item):
	if (item == None):
		return False
	else:
		return True

def zero_patch(n1, n2):
	if n1 == n2:
		return 0
	return 1
	
def brighten(col, amount):
	if len(col) == 3:
		r, g, b = col
		return r + amount, g + amount, b + amount
	if len(col) == 4:
		r, g, b, a = col
		return r + amount, g + amount, b + amount, a
	
def invert_color(col):
	if len(col) == 3:
		r, g, b = col
		return b, r, g
	if len(col) == 4:
		r, g, b, a = col
		return b, r, g, a