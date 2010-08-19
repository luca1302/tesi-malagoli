# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$1-ago-2010 14.16.51$"

from taburoute import *
from trucks import trucks_number
from customer import customers

import sys

if __name__ == "__main__":
    print(sys.argv[1],sys.argv[2]);
    print(taburoute(set(range(len(customers)))-set([0]),trucks_number(),50,lenght=int(sys.argv[1]),elapsed=int(sys.argv[2])));
