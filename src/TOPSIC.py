#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 10:30:44 2022

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

class frmTOPSIC(QWidget):
    def __init__(self,**kwargs):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        
        self._add_widget('_lblTitle',QLabel('TOPSIC METHOD',self),[0,0,1,6])     
        self._add_widget('_lblAlternatives',QLabel('Input list of alternatives',self),[1,0,1,2])
        self._add_widget('_txtAlternatives',QLineEdit('',self),[1,2,1,4])  
        self._add_widget('_lblAttributes',QLabel('Input list of attributes',self),[2,0,1,2])
        self._add_widget('_txtAttributes',QLineEdit('',self),[2,2,1,4])  
        
        self._add_widget('_lblProperties',QLabel('Input list of properties',self),[3,0,1,2])
        self._add_widget('_txtProperties',QLineEdit('',self),[3,2,1,4])  
        
        self._add_widget('_lblWeights',QLabel('Input list of weights',self),[4,0,1,2])
        self._add_widget('_txtWeights',QLineEdit('',self),[4,2,1,4])  
        
        self._add_widget('_lblSelection',QLabel('Normalization method',self),[5,0,1,2])
        self._add_widget('_cmbSelections',QComboBox(self),[5,2,1,4])
        self._cmbSelections.addItems(['[1]:Squareroot Method','[2]:Max-Min Difference Method',])
        self._cmbSelections.setEditable(False)
        self._add_widget('_chkPlot',QCheckBox("PlotGraph",self),[6,0,1,2])
        
        self._add_widget('_btnRun',QPushButton("Run",self),[6,3,1,1],func=self._Run)
        self._add_widget('_btnSave',QPushButton("Save",self),[6,4,1,1],func=self._SaveResult)
        self._add_widget('_btnClose',QPushButton("Close",self),[6,5,1,1],func=self._Close)
        self._add_widget('_txtResult',QTextEdit('',self),[7,0,10,6])  
       
        
        self._lblTitle.setFont(QFont("Times",20, QFont.Bold))
        self._lblTitle.setStyleSheet("color: blue")
        self._lblTitle.setAlignment(Qt.AlignCenter)
        self._layout.setVerticalSpacing(10)
        self._layout.setHorizontalSpacing(10)
        self.setWindowTitle('TOPSIC Method')        
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
    def _SaveResult(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 
            "Save File", "", "All Files(*);;Text Files(*.txt)", options = options)
        if fileName:
            with open(fileName, 'w') as f:
                f.write(self._txtResult.toPlainText())
                
    def _Run(self):
        self._GetData()
        if self._chkPlot.isChecked():
            self.plot_graph()
        self._TOPSIC()
        
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
        
    def _TOPSIC(self):
        self._txtResult.clear()
        self._txtResult.append("TOPSIC Method Report \n")
        self._txtResult.append("Alternative list \n"+str(self.ALTS) + "\n")
        self._txtResult.append("Attribute list \n" + str(self.ATBS) + "\n")
        self._txtResult.append("Attribute prop \n" +str(self.ATB_PROP) + "\n")
        self._txtResult.append("Weight list \n" + str(self.WEIGHTS) + "\n")
        self._txtResult.append("The survey matrix \n" + str(self.SURVEY) +"\n")
      
    
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

    def normV2(self,mat):
        self._txtResult.append("The normalization method \n Max-Min Difference \n")
        new_mat=copy.deepcopy(mat)
        new_mat2=copy.deepcopy(mat)
        ref=[]
        for c in range(self.NUM_ATBS):
            min_val=np.min(new_mat[:,c])
            max_val=np.max(new_mat[:,c])
            ref.append((min_val,max_val))
            for r in range(self.NUM_ALTS):  
                new_mat[r,c]=self.WEIGHTS[c]*(new_mat[r,c]-min_val)/(max_val-min_val)
                new_mat2[r,c]=(new_mat2[r,c]-min_val)/(max_val-min_val)
              
        print("Reference :",ref)
        return new_mat, new_mat2

    def findPNIS(self,mat):
        PIS=[]
        NIS=[]
        for c in range(self.NUM_ATBS):
            if(self.ATB_PROP[c]==1):
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
    
    def _Close(self):      
        self.close()
        #QApplication.quit()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=frmTOPSIC()
    sys.exit(app.exec_())