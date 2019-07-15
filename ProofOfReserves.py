# -*- coding: utf-8 -*-
# Author    :   RenrenBit Lab
# Date      :   2019.7.1
# Version   :   1.0

import hashlib
import random

HASHLEN = 8

class MerkelNode:
    def __init__(self, hashstr, amount, level):
        self.hashid = hashstr
        self.amount = amount
        self.level = level

def hash_func(userid, nonce, amount):
    inputstr = userid + str(nonce) + str(amount)
    hashstr  = hashlib.sha256(inputstr.encode("utf-8"))
    hashid   = hashstr.hexdigest()[0:HASHLEN * 2]
    return hashid

def build_merkle_tree(input, output, outtree):
    # step 1: input and output
    filep = open(input)
    totalreserves = filep.readlines()
    filep.close()
    fileoutput = open(output, 'w')
    fileouttree = open(outtree, 'w')
    #step 2: build node
    nodelist = []
    level = 0
    totalsum = 0
    for userdata in totalreserves:
        userid, num = userdata.split(',')
        amount = int(num)
        nonce = random.randint(1, 65536)
        # hash
        hashid = hash_func(userid, nonce, amount)
        #write
        outstr = userid + ',' + str(amount) + ',' + str(nonce) + ',' + hashid + '\n'
        fileoutput.write(outstr)
        #write
        outstr = str(level) + ',' + str(amount) + ',' + hashid + '\n'
        fileouttree.write(outstr)
        # create node
        node = MerkelNode(hashid, amount, 0)
        nodelist.append(node)
        totalsum = totalsum + amount

    print("Total User:\t", len(nodelist))
    print("Total assets:\t", totalsum)

    parentslist = []
    level = 1
    
    #step 3: build  merkel tree
    # create empty node
    nonce = random.randint(1, 65536)
    hashid = hash_func("EMPTY_NODE_STRING", nonce, 0)
    emptynode = MerkelNode(hashid, 0, 0)

    while len(nodelist) > 1:
        plen = len(nodelist)
        if plen % 2 == 1:  #padding node
            paddingnode = emptynode
            paddingnode.level = nodelist[0].level
            nodelist.append(paddingnode)
            #write
            outstr = str(paddingnode.level) + ',' + str(paddingnode.amount) + ',' + paddingnode.hashid + '\n'
            fileouttree.write(outstr)
        index = 0
        for node in nodelist:
            if index % 2 == 1:
                parentnode = []
                sum_amount = nodelist[index - 1].amount + nodelist[index].amount
                # hash(amount +  hashid_left +  hashid_right)[0:16]
                inputstr = str(sum_amount) + nodelist[index - 1].hashid + nodelist[index].hashid
                hashstr = hashlib.sha256(inputstr.encode("utf-8"))
                hashid = hashstr.hexdigest()[0:HASHLEN * 2]
                # write
                outstr = str(level) + ',' + str(sum_amount) + ',' + hashid + '\n'
                fileouttree.write(outstr)
                # add node
                parentnode = MerkelNode(hashid, sum_amount, level)
                parentslist.append(parentnode)
            index = index + 1
        nodelist = parentslist
        parentslist = []
        level = level + 1

    fileoutput.close()
    fileouttree.close()

if __name__ == "__main__":
    build_merkle_tree("inputs.txt", "2.txt", "3.txt")