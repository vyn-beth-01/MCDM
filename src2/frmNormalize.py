#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:33:27 2024

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
from frmRank import *

class frmNormalize(QWidget):
    def __init__(self,**kwargs):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        self.data=kwargs['data_obj']
        
        self.ALTS=self.data['ALTS']
        self.NUM_ALTS=self.data['NUM_ALTS']
        self.ATBS=self.data['ATBS']
        self.NUM_ATBS=self.data['NUM_ATBS']
        self.ATB_PROP=self.data['ATB_PROP']
        self.WEIGHTS=self.data['WEIGHTS']
        self.SURVEY=self.data['SURVEY']
        
        self.norm_obj={}
        self.norm_obj['ALTS']=self.ALTS
        self.norm_obj['NUM_ALTS']=self.NUM_ALTS
        self.norm_obj['ATBS']=self.ATBS
        self.norm_obj['NUM_ATBS']=self.NUM_ATBS
        self.norm_obj['WEIGHTS']=self.WEIGHTS
        self.norm_obj['RAW_PROP']=self.ATB_PROP
        self.norm_obj['RAW_SURVEY']=self.SURVEY
        
        self._add_widget('_lblTitle',QLabel('Normalize',self),[0,0,1,6])     
        self._add_widget('_lblSelection',QLabel('Normalization Method',self),[1,0,1,2])
        self._add_widget('_cmbSelections',QComboBox(self),[1,2,1,4])
        self._cmbSelections.addItems(['[0]: Do nothing','[1]: Sum Square','[2]: MaxCol/Val or Val/MinCol',
                                      '[3]: Max-Min Difference 1','[4]: Max-Min Difference 2'])
        self._cmbSelections.setEditable(False)
        self._cmbSelections.currentIndexChanged.connect(self._onChange)
        
       
        self._add_widget('_lblExplain',QLabel("Fromula: None",self),[2,0,2,6])
        self._add_widget('_btnNorm',QPushButton("Normalization",self),[4,2,1,1],func=self._Norm)
        self._add_widget('_btnClear',QPushButton("Clear",self),[4,3,1,1],func=self._Clear)
        self._add_widget('_btnRank',QPushButton("Send To Rank",self),[4,4,1,1],func=self._SendToRank)
        self._add_widget('_btnClose',QPushButton("Close",self),[4,5,1,1],func=self._Close)
        self._add_widget('_txtResult',QTextEdit('',self),[5,0,10,6])  
       
       
        self._lblTitle.setFont(QFont("Times",20, QFont.Bold))
        self._lblTitle.setStyleSheet("color: blue")
        self._lblTitle.setAlignment(Qt.AlignCenter)
        self._layout.setVerticalSpacing(10)
        self._layout.setHorizontalSpacing(10)
        self.setWindowTitle('Normalize Data')        
        self.setLayout(self._layout)
        self.setFixedSize(600,500)
        
        #self.openDatabase()
        self.setWindowState(Qt.WindowActive)
        self.show()
        
        
        
        
    def _add_widget(self,comp,item,pos,**kwargs):
        self .__setattr__(comp,item) 
        self._layout.addWidget(getattr(self,comp),pos[0],pos[1],pos[2],pos[3])
        if 'func' in kwargs:
            getattr(self,comp).clicked.connect(kwargs['func']) 
            
    def _Clear(self):
        self._txtResult.clear()
        self.norm_obj['NORM_MATRIX']=''
        self.norm_obj['WNORM_MATRIX']=''
        self.norm_obj['ATB_PROP']=''
        
    def _SendToRank(self):
        self.frmRank=frmRank(norm_obj=self.norm_obj)
        self.frmRank.move(2,200)
            
    def _Norm(self):
        ind=self._cmbSelections.currentIndex()
        if ind==0:
            self.m0_method()
        if ind==1:
            self.m1_method()
        if ind==2:
            self.m2_method()
        if ind==3:
            self.m3_method()   
        if ind==4:
            self.m4_method() 
   
    
    
    def _Close(self):      
        self.close()
        QApplication.quit()
    def _onChange(self):
        ind=self._cmbSelections.currentIndex()
        if ind==0:
            self._lblExplain.setText("Formula: None")
        if ind==1:
            self._lblExplain.setText("Formula: \u221A(x<sub>ac</sub><sup>2</sup>/\u2211<sub>c</sub>(x<sub>ac</sub><sup>2</sup>))")
        if ind==2:
            self._lblExplain.setText("Ben: x<sub>ac</sub>/x<sup>max</sup><sub>c</sub> -- Cost: x<sup>min</sup><sub>c</sub>/x<sub>ac</sub>")
        if ind==3:
            self._lblExplain.setText("Formula: (x<sub>ac</sub>-x<sup>min</sup><sub>c</sub>)/(x<sup>max</sup><sub>c</sub>-x<sup>min</sup><sub>c</sub>)")
        if ind==4:
            self._lblExplain.setText("Ben:(x<sub>ac</sub>-x<sup>min</sup><sub>c</sub>)/(x<sup>max</sup><sub>c</sub>-x<sup>min</sup><sub>c</sub>) -- Cost: (x<sup>max</sup><sub>c</sub>-x<sub>ac</sub>)/(x<sup>max</sup><sub>c</sub>-x<sup>min</sup><sub>c</sub>)")
    def m0_method(self):
        self._txtResult.clear()
        self._txtResult.append("The normalization method \n Do Nothing \n")
        
        no_w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        for c in range(self.NUM_ATBS):
            for r in range(self.NUM_ALTS):
                no_w_mat[r,c]=self.SURVEY[r,c]
                w_mat[r,c]=self.WEIGHTS[c]*no_w_mat[r,c]
                
                    
        
        self.norm_obj['NORM_MATRIX']=no_w_mat
        self.norm_obj['WNORM_MATRIX']=w_mat  
        self.norm_obj['ATB_PROP']=self.ATB_PROP
      
        self.printReport()
    
    def m1_method(self):
        self._txtResult.clear()
        self._txtResult.append("The normalization method \n Squareroot Method \n")
        
        no_w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        for c in range(self.NUM_ATBS):
            val=np.sqrt(np.dot(self.SURVEY[:,c],self.SURVEY[:,c]))
            print(val)
            for r in range(self.NUM_ALTS):
                no_w_mat[r,c]=1/val*self.SURVEY[r,c]
                w_mat[r,c]=self.WEIGHTS[c]*no_w_mat[r,c]
                
                    
        
        self.norm_obj['NORM_MATRIX']=no_w_mat
        self.norm_obj['WNORM_MATRIX']=w_mat  
        self.norm_obj['ATB_PROP']=self.ATB_PROP
      
        self.printReport()
    
    def m2_method(self):
       self._txtResult.clear()
       self._txtResult.append("The normalization method \n MaxCol/Val or Val/MinCol: \n")
       no_w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
       w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
       
       for c in range(self.NUM_ATBS):
           max_val=np.max(self.SURVEY[:,c])
           min_val=np.min(self.SURVEY[:,c])
           for r in range(self.NUM_ALTS):
               if(self.ATB_PROP[c]==1):
                   no_w_mat[r,c]=self.SURVEY[r,c]/max_val
                   w_mat[r,c]=self.WEIGHTS[c]*no_w_mat[r,c]
               else:
                   no_w_mat[r,c]=min_val/self.SURVEY[r,c]
                   w_mat[r,c]=self.WEIGHTS[c]*no_w_mat[r,c]
       
       self.norm_obj['NORM_MATRIX']=no_w_mat
       self.norm_obj['WNORM_MATRIX']=w_mat  
       self.norm_obj['ATB_PROP']=self.NUM_ATBS*[1]
      
       self.printReport()
       
    def m3_method(self):
        self._txtResult.clear()
        self._txtResult.append("The normalization method \n Max-Min Difference Method \n")
        no_w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        ref=[]
        for c in range(self.NUM_ATBS):
            min_val=np.min(self.SURVEY[:,c])
            max_val=np.max(self.SURVEY[:,c])
            ref.append((min_val,max_val))
            for r in range(self.NUM_ALTS):
                no_w_mat[r,c]=(self.SURVEY[r,c]-min_val)/(max_val-min_val)
                w_mat[r,c]=self.WEIGHTS[c]*no_w_mat[r,c]
               
        self.norm_obj['NORM_MATRIX']=no_w_mat
        self.norm_obj['WNORM_MATRIX']=w_mat  
        self.norm_obj['ATB_PROP']=self.ATB_PROP
        self.printReport()
        
    def m4_method(self):
        self._txtResult.clear()
        self._txtResult.append("The normalization method \n Max-Min Difference Method \n")
        no_w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        w_mat=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        ref=[]
        for c in range(self.NUM_ATBS):
            min_val=np.min(self.SURVEY[:,c])
            max_val=np.max(self.SURVEY[:,c])
            ref.append((min_val,max_val))
            for r in range(self.NUM_ALTS):
                if self.ATB_PROP[c]==1:
                    no_w_mat[r,c]=(self.SURVEY[r,c]-min_val)/(max_val-min_val)
                    w_mat[r,c]=self.WEIGHTS[c]*no_w_mat[r,c]
                else:
                    no_w_mat[r,c]=(max_val-self.SURVEY[r,c])/(max_val-min_val)
                    w_mat[r,c]=self.WEIGHTS[c]*no_w_mat[r,c]
        self.norm_obj['NORM_MATRIX']=no_w_mat
        self.norm_obj['WNORM_MATRIX']=w_mat  
        self.norm_obj['ATB_PROP']=self.NUM_ATBS*[1]
        self.printReport()
    
    def printReport(self):
        self._txtResult.clear()
        self._txtResult.append(f"The alternatives \n" + str(self.norm_obj['ALTS'])+ "\n")
        self._txtResult.append(f"The criterions \n" + str(self.norm_obj['ATBS'])+ "\n")
        self._txtResult.append(f"The weights \n" + str(self.norm_obj['WEIGHTS'])+ "\n")
        self._txtResult.append(f"The raw criteria property \n" + str(self.norm_obj['RAW_PROP'])+ "\n")
        self._txtResult.append(f"The raw survey\n" + str(self.norm_obj['RAW_SURVEY'])+ "\n")
        self._txtResult.append(f"After Normalization\n")
        self._txtResult.append(f"------------------------------------------\n")
        self._txtResult.append(f"The criteria property:\n" + str(self.norm_obj['ATB_PROP'])+ "\n")
        
        self._txtResult.append(f"The norm. matrix: \n" + str(self.norm_obj['NORM_MATRIX'])+ "\n")
        self._txtResult.append(f"The weight norm. matrix: \n" + str(self.norm_obj['WNORM_MATRIX'])+ "\n")
        


