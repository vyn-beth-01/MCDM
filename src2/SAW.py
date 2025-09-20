#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:09:02 2024

@author: kyphuc
"""

import sys
import time
import os
import copy
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

class SAW():
    def __init__(self,**kwargs):
        self.obj=kwargs['norm_obj']
        self.board=kwargs['board']
        
        self.ALTS=self.obj['ALTS']
        self.NUM_ALTS=self.obj['NUM_ALTS']
        self.ATBS=self.obj['ATBS']
        self.NUM_ATBS=self.obj['NUM_ATBS']
        self.ATB_PROP=self.obj['ATB_PROP']
        self.RAW_PROP=self.obj['RAW_PROP']
        self.RAW_SURVEY=self.obj['RAW_SURVEY']
        self.NORM_MATRIX= self.obj['NORM_MATRIX']
        self.WNORM_MATRIX=self.obj['WNORM_MATRIX']
        self.WEIGHTS=self.obj['WEIGHTS']
        
        self.scores=None
        
        
    def findSAW(self):
        P=[]
        for a in range(self.NUM_ALTS):
            p_val=0
            for c in range(self.NUM_ATBS):
                p_val+=self.WEIGHTS[c]*self.NORM_MATRIX[a,c]
            P.append(p_val)
        return P
    def Rank(self):
        self.scores=self.findSAW()
        self.printReport()
            
    def printReport(self):
        self.board.clear()
        self.board.append("SAW method report \n")
        self.board.append("Alternative: \n" + str(self.ALTS) + "\n")
        self.board.append("Criteria: \n" + str(self.ATBS) + "\n")
        self.board.append("Raw prop: \n" + str(self.RAW_PROP) + "\n")
        self.board.append("Raw survey: \n" + str(self.RAW_SURVEY) + "\n")
        self.board.append("Weights: \n" + str(self.WEIGHTS) + "\n")
        self.board.append("After normalization: \n")
        self.board.append("------------------------------------\n")
        self.board.append("Property: \n" + str(self.ATB_PROP) + "\n")
        self.board.append("Norm matrix: \n" + str(self.NORM_MATRIX) + "\n")
        self.board.append("Weighted Norm matrix: \n" + str(self.WNORM_MATRIX) + "\n")
        self.board.append("Performance: \n" + str(self.scores) + "\n")
       
        