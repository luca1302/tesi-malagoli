# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$1-ago-2010 14.16.51$"

from gts import *;
from trucks import trucks_number
from customer import customers

if __name__ == "__main__":
    print(gts(set(range(len(customers)))-set([0]),trucks_number(),{}));
