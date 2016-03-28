#FINAL VARS
#			Node_size
#			Edge_width
#			Edge_knob/bolt/handle_size

#class (FloatLayout)

#contains 	
#
#INSTANCE VARS
#			data_output (place where to send info from user interactions)
#			NodeWigets[] (place at same index as node id)
#			EdgeWidgets[] (place at same index as edge id)
#
#			Banner class (for titles) (just use bubbles?)
#
#			Node class
#						button
#						tag
#						pos
#						color (possibly going to have option of loading from file and writting to file)
#						on_select(): archetype method to be determined by override in the instantiation class
#
#			Edge class
#						button
#						tag
#						pos1, pos2
#						color (possibly going to have option of loading from file and writting to file)
#						on_select(): archetype method to be determined by override in the instantiation class
#
#			draw():
#					run through both Node and Edge Widgets and draw
#
#Tree class
#On build, in moment of drawing line between two nodes, create edge and add it to the list at aformentionned
#index. info about edge is taken from the head node's info list in a list called "edge_to". 
#If "edge_to" is None, don't put any data. (usually, if its the root, an edge won't be created anyway so that
#solves that problem)
#
#each node and edge only has color and position.
#it's the exterior  controller that on click of a node or edge knows to go look for info in the data version
#of the thing and add a bubble on the image