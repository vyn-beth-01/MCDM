#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:59:44 2024

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

class ELECTRE():
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
        
        self.con_mat=None
        self.dis_mat=None
        self.c_bar=None
        self.d_bar=None
        self.con_ind_mat=None
        self.dis_ind_mat=None 
        self.rank_ind_mat=None
        
    def findELECTRE(self):
        self.con_mat=self._get_concordance()
        self.dis_mat=self._get_discordance()
        self.c_bar, self.d_bar=self._get_threshold()
        self.con_ind_mat, self.dis_ind_mat, self.rank_ind_mat=self._get_index_matrix()
    def Rank(self):
        self.findELECTRE()
        self.printReport()
    
    def _get_concordance(self):
        print(self.ATB_PROP)
        con_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                r_score=self.NORM_MATRIX[r,:]
                c_score=self.NORM_MATRIX[c,:]
                comp=list(map(lambda x,y:np.sign(x-y), r_score ,c_score))
           
                concor_score=0
                for i in range(self.NUM_ATBS):
                    if comp[i] >=0 and self.ATB_PROP[i]==1:
                        concor_score+=self.WEIGHTS[i]
                    if comp[i] <=0 and self.ATB_PROP[i]==-1:
                        concor_score+=self.WEIGHTS[i]
                con_mat[r,c]=concor_score
        return con_mat
    
    def _get_discordance(self):
        dis_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        diff=[0]*self.NUM_ATBS
        for j in range(self.NUM_ATBS):
            min_val=min(self.NORM_MATRIX[:,j])
            max_val=max(self.NORM_MATRIX[:,j])
            diff[j]=max_val-min_val
            
        
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                
                r_score=self.NORM_MATRIX[r,:]
                c_score=self.NORM_MATRIX[c,:]
                dis_val=max(list(map(lambda x,y,z,d:z*(y-x)/d, r_score ,c_score,self.ATB_PROP,diff)))       
                    
                
      
                if dis_val >=0 and r!=c:
                    dis_mat[r,c]=dis_val
                if dis_val <0 :
                    dis_mat[r,c]=0                    
        return dis_mat
    
    def _get_index_matrix(self):
        con_ind_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        dis_ind_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        rank_ind_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if r!=c and self.con_mat[r,c]>=self.c_bar:
                    con_ind_mat[r,c]=1
                if r!=c and self.dis_mat[r,c]<=self.d_bar:
                    dis_ind_mat[r,c]=1
                if r!=c and con_ind_mat[r,c]==1 and dis_ind_mat[r,c]==1:
                    rank_ind_mat[r,c]=1
        return con_ind_mat, dis_ind_mat, rank_ind_mat
        
    def _get_threshold(self):
        c_bar=0;
        d_bar=0;
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if r!=c:
                    c_bar+=self.con_mat[r,c]
                    d_bar+=self.dis_mat[r,c]
        c_bar=c_bar/(self.NUM_ALTS*(self.NUM_ALTS-1))
        d_bar=d_bar/(self.NUM_ALTS*(self.NUM_ALTS-1))
        return c_bar, d_bar

    
    def _Interprete(self):
        self.board.append("Outrank results \n")
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if self.rank_ind_mat[r,c]==1:
                    self.board.append(f"{self.ALTS[r]} outrank {self.ALTS[c]} \n")
    
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
        
        self.board.append("Concordance mattrix: \n" + str(self.con_mat) + "\n")
        self.board.append("Discordance matrix: \n" + str(self.dis_mat) + "\n")
        self.board.append("C bar: \n" + str(self.c_bar) + "\n")
        self.board.append("D bar: \n" + str(self.d_bar) + "\n")
        self.board.append("Con Ind Matrix: \n" + str(self.con_ind_mat) + "\n")
        self.board.append("Dis Ind Matrix: \n" + str(self.dis_ind_mat) + "\n")
        self.board.append("Rank Ind Matrix: \n" + str(self.rank_ind_mat) + "\n")
        self._Interprete()