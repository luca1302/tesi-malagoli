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
	#self.output=SSHCommand(self.username,self.host,self.password,"nice python /home/davide/tesi-malagoli/gts2/src/run.py {0} {1}".format(self.gene1,self.gene2)).launch();

def initialize_population(range1,range2,n):

	pop=[];
#	for x in range(range1[0],range1[1]+1):
#		for y in range(range2[0],range2[1]+1):
#			pop+=[(x,y)];
	for x in range(range1[0]+1):
		for y in range(range2[0],range2[1]+1):
			pop+=[(x,y)];

	for x in range(range1[0],range1[1]+1):
		for y in range(range2[0]+1):
			pop+=[(x,y)];
	
	return sample(pop,min(len(pop),n-1))+[(0,1)];

def launch_childs(pop,password):
	#pop=[(0,1),(0,1)];
	#hosts=['davide-laptop'];
	#hosts=hosts.hosts;
	shuffle(hosts);
	#username='davide';
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
			r_list+=[tuple([float(x) for x in g.output.split('\r\n')[0].split(' ')])];

	return r_list;

def calculate_distance(r_list,lenght_desired,elapsed_desired):
	#print(r_list);	
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
	for g1,g2,l,e,f in r_list:
		distance=sqrt((lenght_desired-l)**2+(elapsed_desired-e)**2);
		distance+=100000*f
		if distance in results:
			results[distance]+=[(int(g1),int(g2),f)];
		else:
			results[distance]=[(int(g1),int(g2),f)];
	
	#print(results);	
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
		value=1-((dist)/dist_tot);
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
	print(fitness2);
	#return fitness;
	return fitness2;

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
		#print('iterazione');
		rand=uniform(0,1);
	
		t=0;
		for key in keys:
			t+=key[0];
			if(t>=rand):
				#print(fitness[key[0]][key[1]]);
				selected+=[fitness[key[0]][key[1]]];
				break;
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
	#print('xover starts');
	#print(a,b);
	if uniform(0,1)<crossover_prob:
		a,b=(b,a);
	#print(a,b);
	if mutation(mutation_prob):
		if uniform(0,1)<0.5:
			a=switch(a);
		else:
			b=switch(b);
	#print(a,b);
	#print('xover ends');
	return a,b;

def bit_exchange(s1,s2,c_p,m_p):
	#print('bit_exchange starts');
	l1=len(s1);
	l2=len(s2);
	#print(s1,s2);

	if(l1<l2):
		s1,s2,l1,l2=(s2,s1,l2,l1);

	assert(l1>=l2);
	
	diff=l1-l2;
	#print(s1,s2,diff);
	for k in range(diff):
		s1[k],s2_k=xover(s1[k],'0',crossover_prob,mutation_prob);
		s2[k:k]=[s2_k];
	#print(s1,s2);
	for k in range(l1-diff):
		s1[diff+k],s2[diff+k]=xover(s1[diff+k],s2[diff+k],crossover_prob,mutation_prob);
	#print(s1,s2);
	#print('bit_exchange ends');
	return s1,s2; 

def crossover(couple1,couple2,crossover_prob,mutation_prob):
	g1_1=list(bin(couple1[0])[2:]);
	g2_1=list(bin(couple1[1])[2:]);
	g1_2=list(bin(couple2[0])[2:]);
	g2_2=list(bin(couple2[1])[2:]);
	#print('crossover');
	#print(g1_1,g2_1,g1_2,g2_2);

	g1_1_,g1_2_=bit_exchange(g1_1,g1_2,crossover_prob,mutation_prob);
	g2_1_,g2_2_=bit_exchange(g2_1,g2_2,crossover_prob,mutation_prob);

	#print(g1_1_,g2_1_,g1_2_,g2_2_);
	#print('crossover ends');
	g1_1_=int("".join(g1_1_),2);
	g1_2_=int("".join(g1_2_),2);
	g2_1_=int("".join(g2_1_),2);
	g2_2_=int("".join(g2_2_),2);

	return [(g1_1_,g2_1_),(g1_2_,g2_2_)];

def breed(selected,crossover_prob,mutation_prob):

	pop=[];
	for k in range(len(selected)/2):
		pop+=crossover(selected[k],selected[k+1],crossover_prob,mutation_prob);
	#print(pop);
	return pop;

def select_and_breed(fitness,num,pop_tot,crossover_prob,mutation_prob):
	selected=select(fitness,num);
	#return breed(selected,crossover_prob,mutation_prob);
        pop2=breed(selected,crossover_prob,mutation_prob);
        #sorted_keys=sorted(fitness.keys(),reversed=True);
        assert(len(pop2)<=pop_tot);
        #delta_pop=pop_tot-len(pop2);
        
        for key in sorted(fitness.keys(),reverse=True):
		for j in range(len(fitness[key])):
                        if len(pop2)>=pop_tot:
                            break;
                        else:
                            pop2+=[(fitness[key][j][0],fitness[key][j][1])];
			
        
        #for index in range(0,len(pop)-len(pop2)):
        #    pop2+=[pop[index]];

        assert(len(pop2)==pop_tot);
        print(pop2);
        return pop2;
            

if __name__ == '__main__':
	seed(a=123456789);
	#password=getpass.getpass('Password: ');
        password=None;

	desired_lenght=float(sys.argv[1]);
	desired_elapsed=float(sys.argv[2]);
	gen_max=int(sys.argv[3]);
	pop_max=100;
	mutation_prob=0.01;
	crossover_prob=0.5;
	
	f=open('results.txt','w');

	pop=initialize_population((0,100),(0,100),pop_max);
	k=0;
	
	while(k<gen_max):
		results=evaluate_fitness(pop,password,desired_lenght,desired_elapsed);
		f.write(str(results));
		pop=select_and_breed(results,pop_max/2,len(pop),crossover_prob,mutation_prob);
		k+=1;
		
        #f=open('results.txt','w');
        f.write(str(evaluate_fitness(pop,password,desired_lenght,desired_elapsed)));
	f.close();
