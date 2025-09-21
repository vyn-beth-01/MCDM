#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:15:48 2024

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

class frmPROMETHEE(QWidget):
    def __init__(self,**kwargs):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        
        self._add_widget('_lblTitle',QLabel('PROMETHEE METHOD',self),[0,0,1,6])     
        self._add_widget('_lblAlternatives',QLabel('Input list of alternatives',self),[1,0,1,2])
        self._add_widget('_txtAlternatives',QLineEdit('',self),[1,2,1,4])  
        self._add_widget('_lblAttributes',QLabel('Input list of attributes',self),[2,0,1,2])
        self._add_widget('_txtAttributes',QLineEdit('',self),[2,2,1,4])  
        
        self._add_widget('_lblProperties',QLabel('Input list of properties',self),[3,0,1,2])
        self._add_widget('_txtProperties',QLineEdit('',self),[3,2,1,4])  
        
        self._add_widget('_lblWeights',QLabel('Input list of weights',self),[4,0,1,2])
        self._add_widget('_txtWeights',QLineEdit('',self),[4,2,1,4])  
        
        self._add_widget('_lblSelection',QLabel('Ranking method',self),[5,0,1,2])
        self._add_widget('_cmbSelections',QComboBox(self),[5,2,1,4])
        self._cmbSelections.addItems(['[1]: Method 1','[2]: Method 2',])
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
        self.setWindowTitle('PROMETHEE Method')        
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
        self._PROMETHEE()
        
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
        
        
        
    def _PROMETHEE(self):
        self._txtResult.clear()
        self._txtResult.append("PROMETHEE Method Report \n")
        self._txtResult.append("Alternative list \n"+str(self.ALTS) + "\n")
        self._txtResult.append("Attribute list \n" + str(self.ATBS) + "\n")
        self._txtResult.append("Attribute prop \n" +str(self.ATB_PROP) + "\n")
        self._txtResult.append("Weight list \n" + str(self.WEIGHTS) + "\n")
        self._txtResult.append("The survey matrix \n" + str(self.SURVEY) +"\n")
      
        
        diffMat,pos_phi,neg_phi,phi=self.calDiff(self.SURVEY,self.H1Func)
        self._txtResult.append("diffMat: \n"+ str(diffMat) +"\n")
        self._txtResult.append("pos_phi: " + str(pos_phi)+ "\n")
        self._txtResult.append("neg_phi: " +str(neg_phi) + "\n")
        self._txtResult.append("phi :" + str(phi) +"\n")
        ind=self._cmbSelections.currentIndex()
        if ind==0:
            pos_P,pos_I,neg_P,neg_I=self.compareMat(pos_phi,neg_phi,phi)
            self._txtResult.append("pos_P \n" + str(pos_P) + "\n")
            self._txtResult.append("pos_I \n" + str(pos_I) + "\n")
            self._txtResult.append("neg_P \n" + str(neg_P) + "\n")
            self._txtResult.append("neg_I \n" + str(neg_I) + "\n")
            P_mat, I_mat, R_mat=self.checkDominate_P1(pos_P,pos_I,neg_P,neg_I)
            self._txtResult.append("Outrank matrix \n" + str(P_mat) + "\n")
            self._txtResult.append("Indifference matrix \n" + str(I_mat) + "\n")
            self._txtResult.append("Uncomparable matrix \n" + str(R_mat) + "\n")
            self.printOut_P1(P_mat,I_mat,R_mat)
        if ind == 1:
            ranks=self.checkDominate_P2(phi)
            self._txtResult.append("Ranks: " + str(ranks) +"\n")
        
    def H1Func(self,X):
##        p=2
##        if X<=0:
##            return 0
##        if X>=0 and X<=2:
##            return X/p
##        if X>=2:
##            return 1
        if X<2:
            return 0
        if X>=2:
            return 1

    def calDiff(self,mat,func):
        diffMat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                for a in range(self.NUM_ATBS):
                    diffMat[r,c]+=self.WEIGHTS[a]*func(self.ATB_PROP[a]*(mat[r,a]-mat[c,a]))
        pos_phi=[]
        neg_phi=[]
        phi=[]
        for a in range(self.NUM_ALTS):
            pos=np.sum(diffMat[a,:])
            neg=np.sum(diffMat[:,a])
            pos_phi.append(pos)
            neg_phi.append(neg)
            phi.append(pos-neg)
        return diffMat,pos_phi,neg_phi,phi

    def compareMat(self,pos_phi,neg_phi,phi):
        pos_P=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        neg_P=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        pos_I=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        neg_I=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if pos_phi[r]>pos_phi[c]:
                    pos_P[r,c]=1
                if pos_phi[r]==pos_phi[c]:
                    pos_I[r,c]=1
                if neg_phi[r]>neg_phi[c]:
                    neg_P[r,c]=1
                if neg_phi[r]==neg_phi[c]:
                    neg_I[r,c]=1
        return pos_P, pos_I, neg_P, neg_I
    
    def checkDominate_P1(self,pos_P, pos_I, neg_P, neg_I):
        P_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        I_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        R_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if pos_P[r,c]*neg_P[c,r] or pos_P[r,c]*neg_I[r,c] or pos_I[r,c]*neg_P[c,r]:
                    P_mat[r,c]=1
                if pos_I[r,c]*neg_I[r,c]:
                    I_mat[r,c]=1
                if (P_mat[r,c]==0) and (I_mat[r,c]==0):
                    R_mat[r,c]=1
        return P_mat, I_mat, R_mat
    
    def printOut_P1(self,P_mat,I_mat,R_mat):
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if P_mat[r,c]==1 and r!=c:
                    self._txtResult.append(f"{self.ALTS[r]} outrank {self.ALTS[c]}")
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if I_mat[r,c]==1 and r!=c:
                    self._txtResult.append(f"{self.ALTS[r]} indifference {self.ALTS[c]}")
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if R_mat[r,c]==1 and r!=c:
                    self._txtResult.append(f"{self.ALTS[r]} uncomparable {self.ALTS[c]}")
                
    
    def printOut_P2(self,P_mat,I_mat,R_mat):
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if P_mat[r,c]==1:
                    self._txtResult.append(f"{self.ALTS[r]} > {self.ALTS[c]}")
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if R_mat[r,c]==1:
                    self._txtResult.append(f"{self.ALTS[r]} is uncomparable to {self.ALTS[c]}")

    def checkDominate_P2(self, phi):
        mydict=dict(zip(self.ALTS,phi))
        ranks= sorted(mydict.items(), key=lambda x:x[1],reverse=True)
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
        #QApplication.quit()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=frmPROMETHEE()
    sys.exit(app.exec_())
    
    
    
    
