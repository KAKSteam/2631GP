###START###

import numpy
import math
from pygraph.classes.digraph import digraph
from loader import load
C = 9
K = 9
prog = 0
step = 9
energy = 9

def FDG(G,x,tol):
	global K
	global prog
	global step
	global energy
	global C
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
		return pow(numpy.subtract(j,i),2)/K
		return pow()
	def dist(a,b):
		zipVector = zip(a, b)
		quar_distance = 0
		for member in zipVector:
			quar_distance += (member[1] - member[0]) ** 2
 
		return math.sqrt(quar_distance)
	###MAIN START###
	converged = False
	#UNTIL CONVERGED FORMULA MAKES ANY SENSE
	iter = 0
	########################################
	while converged != True:
		#pos
		oldx = x
		oldEnergy = energy
		energy = [0,0]
		for i in G.nodes():
			f = [0,0]
			for j in G.node_neighbors[i]:
				force = fa(i,j)
				distance = dist(numpy.array(x[j]),numpy.array(x[i]))
				if distance == 0:
					distance = 0.1
				num = numpy.subtract(j,i)
				mth = ((force/distance) * num)
				f[0] = f[0]+mth
				f[1] = f[1]+mth
			for j in G.nodes():
				if G.nodes().index(i) != G.nodes().index(j):
					d = dist(numpy.array(x[j]),numpy.array(x[i]))
					if d == 0:
						d = 0.1
					p = numpy.divide(fr(i,j),d)
					mth = numpy.multiply(p,(numpy.subtract(numpy.array(j),numpy.array(i))))
					f[0] = f[0]+mth
					f[1] = f[1]+mth
			dis = dist(numpy.array([0,0]),numpy.array(f))
			if dis == 0:
				dis = 0.1
			a = numpy.array([step,step]) + numpy.array(x[i])
			nums = numpy.multiply(a,numpy.divide(numpy.array(f),numpy.array([dis,dis])))
			#print nums
			x[i] = nums
			numb = pow(dist(numpy.array([0,0]),numpy.array(f)),2)
			energy[0] = energy[0] + numb
			energy[1] = energy[1] + numb
			
		step = updateSteplength(step,energy,oldEnergy)
		iter = iter + 1
		if(iter == 10):
			converged = True
	return x

 
plot = FDG(load("EWDGraphFinal.txt"),[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],9)
print plot