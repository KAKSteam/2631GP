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