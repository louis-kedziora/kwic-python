#!/usr/bin/env python3
from collections import OrderedDict
import sys
import re
# Louis Kedziora
# V00820695
# March 12, 2017
# SENG-265/Assignment-3

class Kwic:
    
    def __init__(self, excluded, lines):
        self.excluded = excluded[:]
        self.index_lines = lines[:]
        self.rhs_length = 30;
        self.lhs_length = 20;
# output()
# This method takes no parameters but instead
# uses the elments of the class to build and
# returns the output.
# @Returns - the indexed lines a list
    def output(self):
        ind_dic = {}
        out = []
        for line in self.index_lines:
            if line == "": #Ignore empty lines 
                continue
            line = line.replace("\n", "")
            ind_dic = self.build_index(line, ind_dic)
        ind_dic = OrderedDict(sorted(ind_dic.items()))
        for ele in ind_dic: #Print the dictonary in sorted order
            for kind in ind_dic[ele]:
                out.append(kind)
        return out

# build_index()
# This method takes the current line to work on and 
# the index dictionary to add to. Then, breaks it down into 
# char arrays and goes word by word create a kwic indexed line
# according to the assignment specs.
# @Params  -  takes a line of text and the index dictionary.
# @Returns -  the dictionary with all the words(save the exclusion
#             words) in the line.
    def build_index(self,line, ind_dic):
        line_split = line.split()
        for word in line_split:
            wordl = word.lower()
            if wordl in self.excluded:
                    continue
            if wordl not in ind_dic:
                ind_dic[wordl] = []
            inds = re.search(r'\b%s\b' % word, line,re.IGNORECASE)
            start = inds.start() - (self.lhs_length + 1) # - 21
            end = inds.start() + self.rhs_length + 2 # - 32
            if start < 0:
                start = 0
            edit = line[start : end]
            inds = re.search(r'\b%s\b' % word, edit,re.IGNORECASE)
            if (len(edit) - inds.start()) < self.rhs_length + 2: # < 32
                edit = edit + " "
            if (inds.start()) < self.lhs_length + 1: # < 21
                edit = " " + edit
            p = re.compile(r'\b%s\b' % word, re.IGNORECASE)
            edit = p.sub(word.upper(), edit)
            p = re.compile(r'\b\w+\Z|^\b\w+\b', re.IGNORECASE)
            edit = p.sub("", edit)
            edit = edit.strip()
            last = re.search(r'\b%s\b' % wordl, edit,re.IGNORECASE)
            ind_dic[wordl].append((" " * ((self.rhs_length - 1) - last.start()))  + edit) # 29 -
        return ind_dic
