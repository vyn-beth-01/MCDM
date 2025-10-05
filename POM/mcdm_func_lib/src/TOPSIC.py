#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 04 Oct 2025
@author: vyn
The source has reference from teachers sources. 
"""
import sys
import time
import os
import copy
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import data_normalization as df_normalization

"""
The below method is supported func and main run for method TOPSIS
"""

def TOPSIS_run(raw_df,normalize_method):
    #init variable:
    _txtResults = ""
 
def _SaveResult(data,method,filename=None):
    if not filename:
        # Get the current date and time
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_with_datetime = f"Output_results_{method}{timestamp_str}.txt"
    try:
        with open(filename_with_datetime, "w") as f:
            f.write(data)
        print(f"File '{filename_with_datetime}' created successfully.")
    except IOError as e:
        print(f"Error creating file: {e}")
                
        
    def _GetData(raw_df):
        ALTS = raw_df.index()[:-2] #list of alternatives
        NUM_ALTS=len(ALTS)
        ATBS=raw_df.columns() #list of attributes
        NUM_ATBS=len(ATBS)
        ATB_PROP = raw_df.loc["Prop"].values().tolist() #list of prop
        WEIGHTS=[float(i) for i in raw_df.loc['Weights'].values().tolist()]
        str_lst=[str(i) for i in raw_df.loc['Weights'].values().tolist()]

        return ALTS, NUM_ALTS, ATBS, NUM_ATBS
    
    def normalize_wo_weight(raw_df,normalize_method):

        """
        TBU
        """
        if normalize_method=='Min-Max Scaler':
            norm_df,norm_matrix = df_normalization.minmaxscaler(raw_df,exclude_row=2)
        elif normalize_method=='StandardScaler':
            norm_df,norm_matrix = df_normalization.standardscaler(raw_df,exclude_row=2)
        elif normalize_method=='RobustScaler':
            norm_df,norm_matrix = df_normalization.robustscaler(raw_df,exclude_row=2)

        return norm_df,norm_matrix
    def normalize_w_weight(norm_df,norm_matrix,):

        return
    
    def 









        _txtResults+="TOPSIC Method Report \n"
        _txtResults+="Alternative list \n"+str(self.ALTS) + "\n"
        _txtResults+="Attribute list \n" + str(self.ATBS) + "\n"
        _txtResults+="Attribute prop \n" +str(self.ATB_PROP) + "\n"
        _txtResults+="Weight list \n" + str(self.WEIGHTS) + "\n"
        _txtResults+="The survey matrix \n" + str(self.SURVEY) +"\n"
      
    
        ind=self._cmbSelections.currentIndex()
        if ind==0:
            
            self.norm_mat,self.norm_mat_noweight=self.normV1(self.SURVEY)
        if ind==1:
            
            self.norm_mat,self.norm_mat_noweight=self.normV2(self.SURVEY)
            
        self._txtResult.append("The normalized matrix w/o weights: \n" + str(self.norm_mat_noweight) + "\n")
        self._txtResult.append("The normalized matrix with weights: \n" + str(self.norm_mat) + "\n")
        PIS,NIS=self.findPNIS(self.norm_mat)
        
        self._txtResult.append("PIS: \n" + str(PIS) + "\n")
        self._txtResult.append("NIS: \n" + str(NIS) + "\n")
        
      
        PDist, NDist, PRatio, NRatio=self.distance(self.norm_mat,PIS,NIS)
        self._txtResult.append("PDist: \n" + str(PDist) + "\n")
        self._txtResult.append("NDist: \n" + str(NDist) + "\n")
        self._txtResult.append("C+ Similarity: \n" + str(PRatio) + "\n")
        self._txtResult.append("C- Similarity: \n" + str(NRatio) + "\n")
        val=max(PRatio)
        ind=PRatio.index(val)
        self._txtResult.append("Best alternative: \n" + self.ALTS[ind] + "\n")
        
        
   

    def findPNIS(mat):
        PIS=[]
        NIS=[]
        for c in range(NUM_ATBS):
            if(ATB_PROP[c]==1):
                PIS.append(np.max(mat[:,c]))
                NIS.append(np.min(mat[:,c]))

            else:
                PIS.append(np.min(mat[:,c]))
                NIS.append(np.max(mat[:,c]))
        return PIS,NIS

    def distance(self,mat,PIS,NIS):
        PDist=[]
        NDist=[]
        PRatio=[]
        NRatio=[]

        for r in range(self.NUM_ALTS):
            pos_dist=np.sqrt(np.dot(PIS-mat[r,:],PIS-mat[r,:]))
            neg_dist=np.sqrt(np.dot(NIS-mat[r,:],NIS-mat[r,:]))
            pos_ratio=pos_dist/(pos_dist+neg_dist)
            neg_ratio=neg_dist/(pos_dist+neg_dist)
            PDist.append(pos_dist)
            NDist.append(neg_dist)
            PRatio.append(1-pos_ratio)
            NRatio.append(1-neg_ratio)
        return PDist, NDist, PRatio, NRatio
    
    def plot_graph(self):
        color=['r','g','b','c','m','y','k']
        ax=plt.gca()
        ax.set_title("Alternative Scores")
        ax.set_xticks(list(range(0,len(self.ATBS))),labels=self.ATBS)
        for i in range(len(self.ALTS)):
            plt.plot(self.SURVEY[i,:],marker=".",markersize=15,color=color[i%7],label=self.ALTS[i])

        ax.legend(self.ALTS,loc="upper right")
        plt.show()
    
