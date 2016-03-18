###START###

import numpy
import math
from pygraph.classes.digraph import digraph
from loader import load
C = 9
K = 9
prog = 0
step = 9999999
energy = 9999999
x=[]

def FDG(G,x,tol):
	def updateSteplength(step,e,oe):
		if e<oe:
			prog = prog+1
			if prog>=5:
				prog = 0
				step = step/0.9
		else:
			prog = 0
			step = 0.9*step
	def fa(i,j):
		v = dist(numpy.array(x[j]),numpy.array(x[i]))
		if v == 0:
			v = 0.01
		return -C*pow(K,2)/v
	def fr(i,j):
		return pow(tuple(numpy.subtract(j,i),2))/K
	def dist(a,b):
		zipVector = zip(a, b)
		quar_distance = 0
		for member in zipVector:
			quar_distance += (member[1] - member[0]) ** 2
 
		return math.sqrt(quar_distance)

	converged = False
	#UNTIL CONVERGED FORMULA MAKES ANY SENSE
	iter = 0
	########################################
	while converged != True:
		#pos
		oldx = x
		energy = 9999999
		oldEnergy = energy
		energy = 0
		for i in G.nodes():
			f = 0
			for j in G.node_neighbors[i]:
				print numpy.array(x[j]),numpy.array(x[i])
				f = f+(fa(i,j)/dist(numpy.array(x[j]),numpy.array(x[i]) * (tuple(numpy.subtract(j,i)))))
			for j in G.nodes():
				if G.nodes().index(i) != G.nodes().index(j):
					f = f + (fr(i,j)/dist(numpy.array(x[j]),numpy.array(x[i])) * (tuple(numpy.subtract(numpy.array(j),numpy.array(i)))))
			xi = xi + step * f/dist(numpy.array((0,0)),numpy.array(f))
			energy = energy + pow(dist(numpy.array((0,0)),numpy.array(f)),2)
		step = updateSteplength(step,enegry,oldEnergy)
		iter = iter + 1
		if(iter == 100):
			converged = True
	return x

 
plot = FDG(load("EWDGraphFinal.txt"),[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],9)
print plot