# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"


from threading import Thread
from ssh import SSHCommand
import getpass
import sys
from math import sqrt
from random import shuffle,uniform,seed

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
        #self.output=SSHCommand(self.username,self.host,self.password,"nice python /public/malagoli/tesi-malagoli-read-only/gts2/src/run.py {0} {1}".format(self.gene1,self.gene2)).launch();
	self.output=SSHCommand(self.username,self.host,self.password,"nice python /home/davide/tesi-malagoli/gts2/src/run.py {0} {1}".format(self.gene1,self.gene2)).launch();

def initialize_population(range1,range2,n):
	return [(0,1),(1,0)];

def launch_childs(pop,password):
	#pop=[(0,1),(0,1)];
	hosts=['davide-laptop','davide-laptop'];
	shuffle(hosts);
	username='davide';
	
	assert(len(hosts)==len(pop));
	t_list=[];
	for g,host in zip(pop,hosts):
		print(g,host);
		g=GenThread(g[0],g[1],username,host,password);
		t_list+=[g];
		g.start();
	
	r_list=[];
	for g in t_list:
		g.join();
		r_list+=[tuple([float(x) for x in g.output.split('\r\n')[1].split(' ')])];

	return r_list;

def calculate_distance(r_list,lenght_desired,elapsed_desired):
	print(r_list);	
	#clones={};
	#for g1,g2,l,e in r_list:
	#	#g1,g2,l,e=element;
	#	print(g1,g2,l,e);
	#	clones[(g1,g2)]=[(g1_,g2_,l_,e_) for g1_,g2_,l_,e_ in r_list if (g1==g1_ and g2==g2_)];
	#	if len(clones[(g1,g2)])==1:
	#		del clones[(g1,g2)];
	

	#r_list2=[];
	#len_clones=len(clones);
	#print(len_clones);
	#if(len_clones==0):
	#	r_list2=r_list;
	#else:
	#	for g1,g2,l,e in r_list:
	#		if (g1,g2) not in clones:
	#			r_list2+=[(g1,g2,l,e)];
	#	
	#	for key in clones:
	#		
	#		l_new=0;
	#		e_new=0;
	#		len_clones=len(clones[key]);
	#		for g1,g2,l,e in clones[key]:
	#			l_new+=l;
	#			e_new+=e;
	#			
	#		l_new/=(len_clones);
	#		e_new/=(len_clones);
	#		
	#		r_list2+=[(g1,g2,l_new,e_new)];

	#l_sum=e_sum=0;

	#for g1,g2,l,e in r_list2:
	#	l_sum+=l;
	#	e_sum+=e;

	#print(l_sum,e_sum);
	results={};
	#for g1,g2,l,e in r_list2:
	for g1,g2,l,e in r_list:
		distance=sqrt((lenght_desired-l)**2+(elapsed_desired-e)**2);
		if distance in results:
			results[distance]+=[(int(g1),int(g2))];
		else:
			results[distance]=[(int(g1),int(g2))];
	
	print(results);	
	return results;

def convert_to_fitness(dists):
	print('conversion');
	dist_tot=0;
	for dist,k in dists.items():
		for e in k:
			print(dist,e);
			dist_tot+=dist;

	fitness={};
	for dist,k in dists.items():
		value=1-(dist/dist_tot);
		if value in fitness:
			fitness[value]+=k;
		else:
			fitness[value]=k;
	
	print('end conversion');
	print(fitness);
	return fitness;

def evaluate_fitness(pop,password,l,e):
	r_list=launch_childs(pop,password);
	dists=calculate_distance(r_list,l,e);
	return convert_to_fitness(dists);

def select(fitness,num):
	keys=[];
	for key in fitness:
		for j in range(len(fitness[key])):
			keys+=[(key,j)];	
	
	selected=[];
	for s in range(num):
		print('iterazione');
		rand=uniform(0,1);
	
		t=0;
		for key in keys:
			t+=key[0];
			if(t>=rand):
				print(fitness[key[0]][key[1]]);
				selected+=[fitness[key[0]][key[1]]];
	print(selected);
	return selected;

def mutation(mutation_prob):
	return uniform(0,1)<mutation_prob;

def switch(a):
	assert((a=='1') or (a=='0'));
	if(a=='1'):
		return '0';
	else:
		return '1';

def xover(a,b,crossover_prob,mutation_prob):
	if uniform(0,1)<crossover_prob:
		a,b=(b,a);

	if mutation(mutation_prob):
		if uniform(0,1)<0.5:
			a=switch(a);
		else:
			b=switch(b);

def bit_exchange(s1,s2,c_p,m_p):

	l1=len(s1);
	l2=len(s2);

	if(l1<l2):
		s1,s2,l1,l2=(s2,s1,l2,l1);

	assert(l1>=l2);

	diff=l1-l2;
	for k in range(diff):
		s1[k],s2_k=xover(s1[k],'0',crossover_prob,mutation_prob);
		s2[k:k]=[s2_k];

	for k in range(l1):
		s1[diff+k],s2[diff+k]=xover(s1[k],s2[k],crossover_prob,mutation_prob);
	
	return 

def crossover(couple1,couple2,crossover_prob,mutation_prob):
	g1_1=list(bin(couple1[0])[2:]);
	g2_1=list(bin(couple1[1])[2:]);
	g1_2=list(bin(couple2[0])[2:]);
	g2_2=list(bin(couple2[1])[2:]);

	g1_1_,g1_2_=bit_exchange(g1_1,g1_2,crossover_prob,mutation_prob);
	g2_1_,g2_2_=bit_exchange(g2_1,g2_2,crossover_prob,mutation_prob);
	
	g1_1_=int("".join(g1_1_),2);
	g1_2_=int("".join(g1_1_),2);
	g2_1_=int("".join(g1_1_),2);
	g2_2_=int("".join(g1_1_),2);

	return [(g1_1_,g2_1_),(g1_2_,g2_2_)];

def breed(selected,crossover_prob,mutation_prob):

	pop=[];
	for k in range(len(selected)/2):
		pop+=crossover(selected[k],selected[k+1],crossover_prob,mutation_prob);
	print(pop);
	return pop;

def select_and_breed(fitness,num,crossover_prob,mutation_prob):
	selected=select(fitness,num);
	return breed(selected,crossover_prob,mutation_prob);

if __name__ == '__main__':
	seed(a=123456789);
	password=getpass.getpass('Password: ');

	desired_lenght=float(sys.argv[1]);
	desired_elapsed=float(sys.argv[2]);
	gen_max=int(sys.argv[3]);
	pop_max=50;
	mutation_prob=0.01;
	crossover_prob=0.5;
	
	pop=initialize_population((0,100),(0,100),pop_max);
	k=0;
	while(k<gen_max):
		results=evaluate_fitness(pop,password,desired_lenght,desired_elapsed);
		pop=select_and_breed(results,pop_max,crossover_prob,mutation_prob);
		k+=1;
	
