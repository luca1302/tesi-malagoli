# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$1-ago-2010 14.16.51$"

from taburoute import *
from trucks import trucks_number
from customer import customers


if __name__ == "__main__":
    print(taburoute(set(range(len(customers)))-set([0]),trucks_number(),50));
