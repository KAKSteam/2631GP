# 2631GP
# Repository for a University assignment
# Will be updated as needed
#
# GUIVersion1.py
# Runs the current version of the GUI, current features include the
# ability to clear the canvas (although nothing is drawable yet) and
# exit the program using the appropriate buttons placed in the Menu Bar
# dropdown. Note that next version will have an implemented filechooser
# along with the second dropdown be activated and the debug implemented
#
# loader.py
# Takes in a valid EWD graph or Tree file and loads it into memory.
# Note: Does not have a way of recognizing invalid file types yet. This
# remains to be implemented
#
# TREE VISUALIZER

- Related files:
	
	- TreeVis.kv - associated kv file

	- MovingButtons10.py - python code (name will be changed soon to something more appropriate)
	
		API: For the implementation of the popup menu, some functions had to be outlined. As these
		were few, I've opted for instead just adding comments to the parts of the code that will be
		relevant to this implementation.
		
		These comments are in the:
	
		'''
		
		comment
		
		'''
		
		format
		
		There are 3 relevant sections of the code that have been commented:
		
			1) The spot where you can write whatever and it'll happen on a right click

			2) A variable called popup_menu which I've defined so that you can easily attach your popup to it and access it.

			3) A description of the program hierarchy (at the very end of the code)