#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:54:42 2024

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


class TOPSIS():
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
        
        self.PIS=None
        self.NIS=None
        self.PDist=None
        self.NDist=None
        self.PRatio=None
        self.NRatio=None
        self.bestAlt=None
        
    def findTOPSIS(self):
        self.PIS, self.NIS=self.findPNIS()
        self.PDist, self.NDist, self.PRatio, self.NRatio=self.distance()
        self.findBestAlt()
    def Rank(self):
        self.findTOPSIS()
        self.printReport()
        
    def findPNIS(self):
        PIS=[]
        NIS=[]
        for c in range(self.NUM_ATBS):
            if(self.ATB_PROP[c]==1):
                PIS.append(np.max(self.WNORM_MATRIX[:,c]))
                NIS.append(np.min(self.WNORM_MATRIX[:,c]))

            else:
                PIS.append(np.min(self.WNORM_MATRIX[:,c]))
                NIS.append(np.max(self.WNORM_MATRIX[:,c]))
        return PIS,NIS
    
    def distance(self):
        PDist=[]
        NDist=[]
        PRatio=[]
        NRatio=[]

        for r in range(self.NUM_ALTS):
            pos_dist=np.sqrt(np.dot(self.PIS-self.WNORM_MATRIX[r,:],self.PIS-self.WNORM_MATRIX[r,:]))
            neg_dist=np.sqrt(np.dot(self.NIS-self.WNORM_MATRIX[r,:],self.NIS-self.WNORM_MATRIX[r,:]))
            pos_ratio=pos_dist/(pos_dist+neg_dist)
            neg_ratio=neg_dist/(pos_dist+neg_dist)
            PDist.append(pos_dist)
            NDist.append(neg_dist)
            PRatio.append(1-pos_ratio)
            NRatio.append(1-neg_ratio)
        return PDist, NDist, PRatio, NRatio
    def findBestAlt(self):
        ind=self.PRatio.index(max(self.PRatio))
        self.bestAlt=self.ALTS[ind]
    def printReport(self):
        self.board.clear()
        self.board.append("TOPSIS method report \n")
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
        
        self.board.append("PIS: \n" + str(self.PIS) + "\n")
        self.board.append("NIS: \n" + str(self.NIS) + "\n")
        self.board.append("PDist: \n" + str(self.PDist) + "\n")
        self.board.append("NDist: \n" + str(self.NDist) + "\n")
        self.board.append("PRatio: \n" + str(self.PRatio) + "\n")
        self.board.append("NRatio: \n" + str(self.NRatio) + "\n")
        self.board.append("Best alternative: \n" +str(self.bestAlt)+ "\n")
        
        
        
        
        
        
        