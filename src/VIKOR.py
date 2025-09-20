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

class frmVIKOR(QWidget):
    def __init__(self,**kwargs):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        
        self._add_widget('_lblTitle',QLabel('VIKOR METHOD',self),[0,0,1,6])     
        self._add_widget('_lblAlternatives',QLabel('Input list of alternatives',self),[1,0,1,2])
        self._add_widget('_txtAlternatives',QLineEdit('',self),[1,2,1,4])  
        self._add_widget('_lblAttributes',QLabel('Input list of attributes',self),[2,0,1,2])
        self._add_widget('_txtAttributes',QLineEdit('',self),[2,2,1,4])  
        
        self._add_widget('_lblProperties',QLabel('Input list of properties',self),[3,0,1,2])
        self._add_widget('_txtProperties',QLineEdit('',self),[3,2,1,4])  
        
        self._add_widget('_lblWeights',QLabel('Input list of weights',self),[4,0,1,2])
        self._add_widget('_txtWeights',QLineEdit('',self),[4,2,1,4])  
        
        self._add_widget('_lblNormSelection',QLabel('Normalized method',self),[5,0,1,2])
        self._add_widget('_cmbNormSelections',QComboBox(self),[5,2,1,4])
        self._cmbNormSelections.addItems(['[1]:Max-Min Difference Method','[2]:Squareroot Method',])
        self._cmbNormSelections.setEditable(False)
        
        self._add_widget('_lblSelection',QLabel('Ranking method',self),[6,0,1,2])
        self._add_widget('_cmbSelections',QComboBox(self),[6,2,1,4])
        self._cmbSelections.addItems(['[1]: Simple Rank','[2]: Check Dominate Rank',])
        self._cmbSelections.setEditable(False)
        
        
        
        self._add_widget('_chkPlot',QCheckBox("PlotGraph",self),[7,0,1,2])
        
        self._add_widget('_btnRun',QPushButton("Run",self),[7,3,1,1],func=self._Run)
        self._add_widget('_btnSave',QPushButton("Save",self),[7,4,1,1],func=self._SaveResult)
        self._add_widget('_btnClose',QPushButton("Close",self),[7,5,1,1],func=self._Close)
        self._add_widget('_txtResult',QTextEdit('',self),[8,0,10,6])  
       
       
        
        self._lblTitle.setFont(QFont("Times",20, QFont.Bold))
        self._lblTitle.setStyleSheet("color: blue")
        self._lblTitle.setAlignment(Qt.AlignCenter)
        self._layout.setVerticalSpacing(10)
        self._layout.setHorizontalSpacing(10)
        self.setWindowTitle('VIKOR Method')        
        self.setLayout(self._layout)
        self.setFixedSize(600,500)
        
        #self.openDatabase()
        self.setWindowState(Qt.WindowActive)
        self.show()
        
        self.ALTS=None
        self.NUM_ALTS=0
        self.ATBS=None
        self.NUM_ATBS=0
        self.ATB_PROP=None
        self.WEIGHTS=None
        self.SURVEY=None
        
    def _add_widget(self,comp,item,pos,**kwargs):
        self .__setattr__(comp,item) 
        self._layout.addWidget(getattr(self,comp),pos[0],pos[1],pos[2],pos[3])
        if 'func' in kwargs:
            getattr(self,comp).clicked.connect(kwargs['func'])   
            
    def _Run(self):
        self._GetData()
        if self._chkPlot.isChecked():
            self.plot_graph()
        self._VIKOR()
        
    def _SaveResult(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 
            "Save File", "", "All Files(*);;Text Files(*.txt)", options = options)
        if fileName:
            with open(fileName, 'w') as f:
                f.write(self._txtResult.toPlainText())
                 
    def _GetData(self):
        self.ALTS=self._txtAlternatives.text().split(',')
        self.NUM_ALTS=len(self.ALTS)
        self.ATBS=self._txtAttributes.text().split(',')
        self.NUM_ATBS=len(self.ATBS)
        
        str_lst=self._txtProperties.text().split(',')
        self.ATB_PROP=[int(k) for k in str_lst]
        str_lst=self._txtWeights.text().split(',')
        self.WEIGHTS=[float(k) for k in str_lst]
        self.SURVEY=np.zeros((self.NUM_ALTS,self.NUM_ATBS))
        for r in range(self.NUM_ALTS):
            while True:
                str_text,ok=QInputDialog.getText(self,"Get input",f"Please score {self.ALTS[r]} : ")
                if ok and len(str_text)>0:
                    break      
            str_lst=str_text.split(',')
            self.SURVEY[r,:]=[float(i) for i in str_lst]
        
        
    def _VIKOR(self):
        self._txtResult.clear()
        self._txtResult.append("VIKOR Method Report \n")
        self._txtResult.append("Alternative list \n"+str(self.ALTS) + "\n")
        self._txtResult.append("Attribute list \n" + str(self.ATBS) + "\n")
        self._txtResult.append("Attribute prop \n" +str(self.ATB_PROP) + "\n")
        self._txtResult.append("Weight list \n" + str(self.WEIGHTS) + "\n")
        self._txtResult.append("The survey matrix \n" + str(self.SURVEY) +"\n")
        norm_ind=self._cmbNormSelections.currentIndex()
        if norm_ind==0:
            self.norm_mat,self.norm_mat_noweight=self.normalize(self.SURVEY) 
            
        if norm_ind==1:
            self.norm_mat,self.norm_mat_noweight=self.normV1(self.SURVEY) 
            self._txtResult.append("The normalized matrix w/o weights \n" + str(self.norm_mat_noweight)+"\n")
            self.norm_mat,self.norm_mat_noweight=self.normalize(self.norm_mat_noweight)
        
         
        
        self._txtResult.append("The normalized matrix with weights: \n" + str(self.norm_mat)+"\n")
       
        S,R,Q=self.findLNorm(self.norm_mat)
        self._txtResult.append("S matrix: \n" + str(S) +"\n" )
        self._txtResult.append("R matrix: \n" + str(R) +"\n" )
        self._txtResult.append("Q matrix: \n" + str(Q) +"\n" )
       
      
        ind=self._cmbSelections.currentIndex()
        if ind==0:
            rank=self.simpleRank(Q)
            self._txtResult.append("Simple rank: smaller Q score is better \n" + str(rank)+ "\n")
            
        if ind==1:
            self._txtResult.append("Rank by check dominate")
            self.checkDominate(S, R, Q)
        
    def normalize(self,mat):
        self._txtResult.append("The normalization method \n Max-Min Difference Method \n")
        new_mat=copy.deepcopy(mat)
        new_mat2=copy.deepcopy(mat)
        ref=[]
        for c in range(self.NUM_ATBS):
            min_val=np.min(mat[:,c])
            max_val=np.max(mat[:,c])
            ref.append((min_val,max_val))
            for r in range(self.NUM_ALTS):
                if self.ATB_PROP[c]==1:
                    new_mat[r,c]=self.WEIGHTS[c]*(max_val-mat[r,c])/(max_val-min_val)
                    new_mat2[r,c]=(max_val-mat[r,c])/(max_val-min_val)
                else:
                    new_mat[r,c]=self.WEIGHTS[c]*(mat[r,c]-min_val)/(max_val-min_val)
                    new_mat2[r,c]=(mat[r,c]-min_val)/(max_val-min_val)
        return new_mat, new_mat2
    
    def normV1(self,mat):
        self._txtResult.append("The normalization method \n Squareroot Method \n")
        new_mat=copy.deepcopy(mat)
        new_mat2=copy.deepcopy(mat)
        sqr_col=[]
        for c in range(self.NUM_ATBS):
            val=np.sqrt(np.dot(new_mat[:,c],new_mat[:,c]))
            new_mat[:,c]=self.WEIGHTS[c]*1/val*new_mat[:,c]
            new_mat2[:,c]=1/val*new_mat2[:,c]
            sqr_col.append(val)
        return new_mat,new_mat2

    def findLNorm(self,mat):
        L_1=[]
        L_Inf=[]
        for r in range(self.NUM_ALTS):
            L_1.append(np.sum(mat[r,:]))
            L_Inf.append(np.max(mat[r,:]))
        S_min=np.min(L_1)
        S_max=np.max(L_1)
        R_min=np.min(L_Inf)
        R_max=np.max(L_Inf)
        Q=[]
        v=0.5
        for a in range(self.NUM_ALTS):
            Q.append(v*(L_1[a]-S_min)/(S_max-S_min)+(1-v)*(L_Inf[a]-R_min)/(R_max-R_min))
        return L_1,L_Inf,Q

    def checkDominate(self,S,R,Q):
        sortedQ=copy.deepcopy(Q)
        ind=np.argmin(Q)
        minQ=np.min(Q)
        sortedQ.sort(reverse=False)
        if((sortedQ[1]-sortedQ[0])>= 1/(self.NUM_ALTS-1)) and (S[ind]==np.min(S) or R[ind]==np.min(R)):
            self._txtResult.append("The best alternative is: " +str(self.ALTS[ind]) +"\n")
        if((sortedQ[1]-sortedQ[0])>= 1/(self.NUM_ALTS-1)) and (S[ind]> np.min(S) or R[ind]>np.min(R)):
            best_alt=self.ALTS[ind]
            sec_alt=self.ALTS[Q.index(sortedQ[1])]
            self._txtResult.append("There are 2 alternatives")
            self._txtResult.append("The 1st best alternative is: " + str(best_alt))
            self._txtResult.append("The 2nd best alternative is: "+  str(sec_alt))
        if((sortedQ[1]-sortedQ[0])< 1/(self.NUM_ALTS-1)):
            self._txtResult.append("There are several alternatives")
            for a in range(self.NUM_ALTS):
                if ((Q[a]-minQ) <= 1/(self.NUM_ALTS-1)):
                    self._txtResult.append("The alternative: "+ str(self.ALTS[a]))
        return
    
    def simpleRank(self,Q):
        mydict=dict(zip(self.ALTS,Q))
        ranks= sorted(mydict.items(), key=lambda x:x[1],reverse=False)
        return ranks
    
    def plot_graph(self):
        color=['r','g','b','c','m','y','k']
        ax=plt.gca()
        ax.set_title("Alternative Scores")
        ax.set_xticks(list(range(0,len(self.ATBS))),labels=self.ATBS)
        for i in range(len(self.ALTS)):
            plt.plot(self.SURVEY[i,:],marker=".",markersize=15,color=color[i%7],label=self.ALTS[i])

        ax.legend(self.ALTS,loc="upper right")
        plt.show()
    def _Close(self):      
        self.close()
        QApplication.quit()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=frmVIKOR()
    sys.exit(app.exec_())