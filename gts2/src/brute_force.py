# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"


from threading import Thread
from ssh import SSHCommand
import getpass
import sys
from math import sqrt
from random import shuffle,uniform,seed,sample
from hosts import hosts

class GenThread(Thread):
    def __init__(self,gene1,gene2,username,host,password):
        Thread.__init__(self);
        self.gene1=gene1;
        self.gene2=gene2;
	self.username=username;
	self.host=host;
	self.password=password;
        self.output=None;
    def run(self):
        self.output=SSHCommand(self.username,self.host,self.password,"nice python /public/malagoli/tesi-malagoli-read-only/gts2/src/run.py {0} {1}".format(self.gene1,self.gene2)).launch();

def initialize_population(range1,range2):

	pop=[];
	for x in range(range1[0],range1[1]+1):
		for y in range(range2[0],range2[1]+1):
			pop+=[(x,y)];
	
	
	return pop;

def launch_childs(pop,password):

	#shuffle(hosts);
	#hosts=['gretel.cs.unibo.it',]
	username='malagoli';	

	r_list=[];
	chunk=len(hosts);
	if(len(pop)%len(hosts))==0:
		times=len(pop)/len(hosts);
	else:
		times=(len(pop)/len(hosts))+1;

	for time in range(times):
		pop2=pop[chunk*time:chunk*(time+1)];
		assert(len(hosts)>=len(pop2));
	
		t_list=[];
		for g,host in zip(pop2,hosts):
			print(g,host);
			g=GenThread(g[0],g[1],username,host,password);
			t_list+=[g];
			g.start();
	
		for g in t_list:
			g.join();
			r_list+=[tuple([float(x) for x in g.output.split('\r\n')[1].split(' ')])];

	return r_list;

def calculate_distance(r_list,lenght_desired,elapsed_desired):
	results={};
	
	for g1,g2,l,e in r_list:
		distance=sqrt((lenght_desired-l)**2+(elapsed_desired-e)**2);
		if distance in results:
			results[distance]+=[(int(g1),int(g2))];
		else:
			results[distance]=[(int(g1),int(g2))];
	
		
	return results;

def convert_to_fitness(dists):
	#print('conversion');
	dist_tot=0;
	for dist,k in dists.items():
		for e in k:
			#print(dist,e);
			dist_tot+=dist;

	fitness={};
	for dist,k in dists.items():
		value=1-(dist/dist_tot);
		if value in fitness:
			fitness[value]+=k;
		else:
			fitness[value]=k;

	tot_fit=0;
	for fit,k in fitness.items():
		for e in k:
			tot_fit+=fit;

	fitness2={};
	for fit,k in fitness.items():
		value=fit/tot_fit;
		if value in fitness2:
			fitness2[value]+=k;
		else:
			fitness2[value]=k;
	#print('end conversion');
	#print(fitness);
	#return fitness;
	return fitness2;

def evaluate_fitness(pop,password,l,e):
	r_list=launch_childs(pop,password);
	dists=calculate_distance(r_list,l,e);
	return convert_to_fitness(dists);

if __name__ == '__main__':
	seed(a=123456789);
	password=getpass.getpass('Password: ');

	desired_lenght=float(sys.argv[1]);
	desired_elapsed=float(sys.argv[2]);

	pop=initialize_population((0,100),(0,100));
	
	
	results=evaluate_fitness(pop,password,desired_lenght,desired_elapsed);
		
	f=open('brute_force-results.txt','w');
	f.write(str(results));
	f.close();
