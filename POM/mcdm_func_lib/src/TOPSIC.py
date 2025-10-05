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
# import data_normalization as df_normalization

"""Normalization section"""
from sklearn.preprocessing import MinMaxScaler,StandardScaler,RobustScaler
import pandas as pd
import copy
import numpy as np

def minmaxscaler(df,exclude_row=None):
    """
    This func employ the min-max scaler lib in python to execute the normlization data
    Args:
    - df (dataframe): the raw data frame
    - exclude_row (optional): this is optional fields to specific number of row to exclude out of normalize step
    Return:
    - norm_df: normalize data WITH original exclude row.
    - normalized_data: matrix after normalize
    """

    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    if not exclude_row:
        target_data = df
    else:
        target_data = df.iloc[:-exclude_row,:]
    
    # print(df.shape)
    # print(target_data.shape)
    # Fit and transform the data
    normalized_data = scaler.fit_transform(target_data)
    # print(normalized_data)

    # Convert back to DataFrame (optional)
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns)

    final_normalized_df = pd.concat([normalized_df,df.iloc[-2:,:]])
    return final_normalized_df,normalized_data


def standardscaler(df,exclude_row=None):
    """
    This func employ the standard scaler lib in python to execute the normlization data
    Args:
    - df (dataframe): the raw data frame
    - exclude_row (optional): this is optional fields to specific number of row to exclude out of normalize step
    Return:
    - norm_df: normalize data WITH original exclude row.
    - normalized_data: matrix after normalize
    """

    # Initialize MinMaxScaler
    scaler = StandardScaler()
    if not exclude_row:
        target_data = df
    else:
        target_data = df.iloc[:-exclude_row,:]
    
    # print(df.shape)
    # print(target_data.shape)
    # Fit and transform the data
    normalized_data = scaler.fit_transform(target_data)
    # print(normalized_data)

    # Convert back to DataFrame (optional)
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns)

    final_normalized_df = pd.concat([normalized_df,df.iloc[-2:,:]])
    return final_normalized_df,normalized_data


def robustscaler(df,exclude_row=None):
    """
    This func employ the robust scaler lib in python to execute the normlization data
    Args:
    - df (dataframe): the raw data frame
    - exclude_row (optional): this is optional fields to specific number of row to exclude out of normalize step
    Return:
    - norm_df: normalize data WITH original exclude row.
    - normalized_data: matrix after normalize
    """

    # Initialize MinMaxScaler
    scaler = RobustScaler()
    if not exclude_row:
        target_data = df
    else:
        target_data = df.iloc[:-exclude_row,:]
    
    # print(df.shape)
    # print(target_data.shape)
    # Fit and transform the data
    normalized_data = scaler.fit_transform(target_data)
    # print(normalized_data)

    # Convert back to DataFrame (optional)
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns)

    final_normalized_df = pd.concat([normalized_df,df.iloc[-2:,:]])
    return final_normalized_df,normalized_data



def normV1(df,exclude_row=None):
    if not exclude_row:
        target_data = df
    else:
        target_data = df.iloc[:-exclude_row,:]
    # Get attribute:
    ALTS = target_data.index()[:-2] #list of alternatives
    NUM_ALTS=len(ALTS)
    ATBS=target_data.columns() #list of attributes
    NUM_ATBS=len(ATBS)
    ATB_PROP = target_data.loc["Prop"].values().tolist() #list of prop
    WEIGHTS=[float(i) for i in target_data.loc['Weights'].values().tolist()]
    
    mat = target_data.to_numpy()
    """Normalization SquareRootmethod"""
    new_mat=copy.deepcopy(mat)
    new_mat2=copy.deepcopy(mat)
    sqr_col=[]
    for c in range(NUM_ATBS):
        val=np.sqrt(np.dot(new_mat[:,c],new_mat[:,c]))
        new_mat[:,c]=WEIGHTS[c]*1/val*new_mat[:,c]
        new_mat2[:,c]=1/val*new_mat2[:,c]
        sqr_col.append(val)
    return new_mat,new_mat2

def normV2(mat,NUM_ATBS,NUM_ALTS,WEIGHTS):
    # self._txtResult.append("The normalization method \n Max-Min Difference \n")
    new_mat=copy.deepcopy(mat)
    new_mat2=copy.deepcopy(mat)
    ref=[]
    for c in range(NUM_ATBS):
        min_val=np.min(new_mat[:,c])
        max_val=np.max(new_mat[:,c])
        ref.append((min_val,max_val))
        for r in range(NUM_ALTS):  
            new_mat[r,c]=WEIGHTS[c]*(new_mat[r,c]-min_val)/(max_val-min_val)
            new_mat2[r,c]=(new_mat2[r,c]-min_val)/(max_val-min_val)
            
    print("Reference :",ref)
    return new_mat, new_mat2



"""
The below method is supported func and main run for method TOPSIS
"""

   
def _GetData(raw_df):
    ALTS = raw_df.index()[:-2] #list of alternatives
    NUM_ALTS=len(ALTS)
    ATBS=raw_df.columns() #list of attributes
    NUM_ATBS=len(ATBS)
    ATB_PROP = raw_df.loc["Prop"].values().tolist() #list of prop
    WEIGHTS=[float(i) for i in raw_df.loc['Weights'].values().tolist()]
    str_lst=[str(i) for i in raw_df.loc['Weights'].values().tolist()]

    return ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP

def normalize_wo_w_weight(raw_df,normalize_method):

    """
    TBU
    """
    if normalize_method=='Min-Max Scaler':
        norm_df,norm_matrix = minmaxscaler(raw_df,exclude_row=2)
    elif normalize_method=='StandardScaler':
        norm_df,norm_matrix = standardscaler(raw_df,exclude_row=2)
    elif normalize_method=='RobustScaler':
        norm_df,norm_matrix = robustscaler(raw_df,exclude_row=2)
    elif normalize_method=='SquareRootMethod':
        norm_df,norm_matrix = normV1(raw_df,exclude_row=2)
    return norm_df,norm_matrix

def normalize_w_weight(norm_df,norm_matrix,):

    return 1


def findPNIS(mat,ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP):
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

def distance(mat,PIS,NIS,ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP):
    PDist=[]
    NDist=[]
    PRatio=[]
    NRatio=[]

    for r in range(NUM_ALTS):
        pos_dist=np.sqrt(np.dot(PIS-mat[r,:],PIS-mat[r,:]))
        neg_dist=np.sqrt(np.dot(NIS-mat[r,:],NIS-mat[r,:]))
        pos_ratio=pos_dist/(pos_dist+neg_dist)
        neg_ratio=neg_dist/(pos_dist+neg_dist)
        PDist.append(pos_dist)
        NDist.append(neg_dist)
        PRatio.append(1-pos_ratio)
        NRatio.append(1-neg_ratio)
    return PDist, NDist, PRatio, NRatio

def plot_graph(raw_df,ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP):
    mat = raw_df[:-2,:].to_numpy()
    color=['r','g','b','c','m','y','k']
    ax=plt.gca()
    ax.set_title("Alternative Scores")
    ax.set_xticks(list(range(0,len(ATBS))),labels=ATBS)

    for i in range(len(ALTS)):
        plt.plot(mat[i,:],marker=".",markersize=15,color=color[i%7],label=ALTS[i])

    ax.legend(ALTS,loc="upper right")
    plt.show()


def TOPSIS_run(raw_df,normalize_method):
    ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP= _GetData(raw_df)
    # Call to calculate normalize:
    norm_df_w_weight,norm_df_wo_weight = normalize_wo_w_weight(raw_df,normalize_method)
    # Next step:
    PIS,NIS=findPNIS(norm_df_w_weight,ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP)
    PDist, NDist, PRatio, NRatio=distance(norm_df_w_weight,PIS,NIS,ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP)
    val=max(PRatio)
    ind=PRatio.index(val)

    #Output txt:
    _txtResults = ""
    _txtResults+="TOPSIC Method Report \n"
    _txtResults+="Alternative list \n"+str(ALTS) + "\n"
    _txtResults+="Attribute list \n" + str(ATBS) + "\n"
    _txtResults+="Attribute prop \n" +str(ATB_PROP) + "\n"
    _txtResults+="Weight list \n" + str(WEIGHTS) + "\n"
    _txtResults= _txtResults+"The normalized matrix w/o weights: \n" + str(norm_df_wo_weight) + "\n"
    _txtResults= _txtResults+"The normalized matrix with weights: \n" + str(norm_df_w_weight) + "\n"
    _txtResults= _txtResults+"PIS: \n" + str(PIS) + "\n"
    _txtResults= _txtResults+"NIS: \n" + str(NIS) + "\n"
    _txtResults= _txtResults+"PDist: \n" + str(PDist) + "\n"
    _txtResults= _txtResults+"NDist: \n" + str(NDist) + "\n"
    _txtResults= _txtResults+"C+ Similarity: \n" + str(PRatio) + "\n"
    _txtResults= _txtResults+"C- Similarity: \n" + str(NRatio) + "\n"
    _txtResults= _txtResults+"Best alternative: \n" + ALTS[ind] + "\n"
    
    
    
    return _txtResults


