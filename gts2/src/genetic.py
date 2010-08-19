# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"


from threading import Thread
from ssh import SSHCommand
import getpass
import sys

class GenThread(Thread):
    def __init__(self,id,gene1,gene2,username,host,password):
        Thread.__init__(self);
        self.gene1=gene1;
        self.gene2=gene2;
	self.username=username;
	self.host=host;
	self.password=password;
        self.output=None;
    def run(self):
        self.output=SSHCommand(self.username,self.host,self.password,"nice python /public/malagoli/tesi-malagoli-read-only/gts2/src/run.py {0} {1}".format(self.gene1,self.gene2)).launch();


def initialize_population(range1,range2,n):
	pass;

def launch_childs(pop,password):
	
	t_list=[];
	for host in ['maria.cs.unibo.it','ambrogio.cs.unibo.it']:
		g=GenThread(0,1,0,'malagoli',host,password);
		t_list+=[g];
		g.start();
	
	r_list=[];
	for g in t_list:
		g.join();
		r_list+=g.output.split('\r\n')[1].split(' ');

	return r_list;

def calculate_fitness(r_list,lenght_desired,elapsed_desired):
	
	r_list2=[];
	for g1,g2,l,e in r_list:
		clones=[(g1_,g2_,l_,e_) for g1_,g2_,l_,e_ in r_list if (g1==g1_ and g2==g2_)];
		len_clones=len(clones);
		if(len_clones==0):
			r_list2+=[(g1,g2,l,e)];
		else:
			l_new=l;
			e_new=e;
			
			for g1_,g2_,l_,e_ in clones:
				l_new+=l_;
				e_new+=e_;
				
			l_new/=(len_clones+1);
			e_new/=(len_clones+1);
			
			r_list2+=[(g1,g2,l_new,e_new)];

	l_sum=e_sum=0;

	for g1,g2,l,e in r_list2:
		l_sum+=l;
		e_sum+=e;

	results={};
	for g1,g2,l,e in r_list2:
		fitness=sqrt((lenght_desired-l)**2+(elapsed_desired-e)**2);
		if fitness in results:
			results[fitness]+=[(g1,g2)];
		else:
			results[fitness]=[(g1,g2)];
	
	return results;

def evaluate_fitness(pop,password,l,e):
	#r_list=launch_childs(pop,password);
	return calculate_fitness(r_list,l,e);

if __name__ == '__main__':
	password=getpass.getpass('Password: ');

	desired_lenght=sys.argv[1];
	desired_elapsed=sys.argv[2];
	gen_max=sys.argv[3];

	pop=initialize_population((0,100),(0,100),50);
	k=0;
	while(k<gen_max):
		results=evaluate_fitness(pop,password,desired_lenght,desired_elapsed);
		pop=select_and_breed(results);
		k+=1;
	
