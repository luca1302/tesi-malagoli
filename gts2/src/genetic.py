# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"


from taburoute import taburoute
from trucks import trucks_number
from customer import customers
from threading import Thread
from subprocess import check_output

def gen_thread(Thread):
    def __init__(id,gene1,gene2):
        self.id=id;
        self.gene1=gene1;
        self.gene2=gene2;
        self.output=None;
    def run():
        check_output(['ssh','malagoli@ambrogio.cs.unibo.it']);
        