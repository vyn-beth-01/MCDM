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

class frmELECTRE(QWidget):
    def __init__(self,**kwargs):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        
        self._add_widget('_lblTitle',QLabel('ELECTRE METHOD',self),[0,0,1,6])     
        self._add_widget('_lblAlternatives',QLabel('Input list of alternatives',self),[1,0,1,2])
        self._add_widget('_txtAlternatives',QLineEdit('',self),[1,2,1,4])  
        self._add_widget('_lblAttributes',QLabel('Input list of attributes',self),[2,0,1,2])
        self._add_widget('_txtAttributes',QLineEdit('',self),[2,2,1,4])  
        
        self._add_widget('_lblProperties',QLabel('Input list of properties',self),[3,0,1,2])
        self._add_widget('_txtProperties',QLineEdit('',self),[3,2,1,4])  
        
        self._add_widget('_lblWeights',QLabel('Input list of weights',self),[4,0,1,2])
        self._add_widget('_txtWeights',QLineEdit('',self),[4,2,1,4])  
        
        
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
        self._ELECTRE()
                
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
        
    def _get_concordance(self):
        con_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                r_score=self.SURVEY[r,:]
                c_score=self.SURVEY[c,:]
                comp=list(map(lambda x,y:np.sign(x-y), r_score ,c_score))
                concor_score=0
                for i in range(0,len(comp)):
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
            min_val=min(self.SURVEY[:,j])
            max_val=max(self.SURVEY[:,j])
            diff[j]=max_val-min_val
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                
                r_score=self.SURVEY[r,:]
                c_score=self.SURVEY[c,:]
               
                dis_val=max(list(map(lambda x,y,z,d:z*(y-x)/d, r_score ,c_score,self.ATB_PROP,diff)))
                       
                
                if dis_val >=0 and r!=c:
                    dis_mat[r,c]=dis_val
                if dis_val <0 :
                    dis_mat[r,c]=0                    
        return dis_mat
    
        
    def _ELECTRE(self):
        self._txtResult.clear()
        self._txtResult.append("ELECTRE Method Report \n")
        self._txtResult.append("Alternative list \n"+str(self.ALTS) + "\n")
        self._txtResult.append("Attribute list \n" + str(self.ATBS) + "\n")
        self._txtResult.append("Attribute prop \n" +str(self.ATB_PROP) + "\n")
        self._txtResult.append("Weight list \n" + str(self.WEIGHTS) + "\n")
        self._txtResult.append("The survey matrix \n" + str(self.SURVEY) +"\n")
      
        if self._chkPlot.isChecked():
            self.plot_graph()
        con_mat=self._get_concordance()
        dis_mat=self._get_discordance()
        self._txtResult.append("Concordance matrix \n" + str(con_mat) + "\n")
        self._txtResult.append("Discordance matrix \n" + str(dis_mat) + "\n")
        c_bar, d_bar=self._get_threshold(con_mat,dis_mat)
        self._txtResult.append("Concordance threshold \n" + str(c_bar) + "\n")
        self._txtResult.append("Discordance threshold \n" + str(d_bar) + "\n")
        con_ind_mat, dis_ind_mat, rank_ind_mat=self._get_index_matrix(con_mat, dis_mat, c_bar, d_bar)
        self._txtResult.append("Concordance index matrix \n" + str(con_ind_mat) + "\n")
        self._txtResult.append("Discordance index matrix \n" + str(dis_ind_mat) + "\n")
        self._txtResult.append("Outrank index matrix \n" + str(rank_ind_mat) + "\n")
        self._Interprete(rank_ind_mat)
    def _get_index_matrix(self,con_mat,dis_mat,c_bar,d_bar):
        con_ind_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        dis_ind_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        rank_ind_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if r!=c and con_mat[r,c]>=c_bar:
                    con_ind_mat[r,c]=1
                if r!=c and dis_mat[r,c]<=d_bar:
                    dis_ind_mat[r,c]=1
                if r!=c and con_ind_mat[r,c]==1 and dis_ind_mat[r,c]==1:
                    rank_ind_mat[r,c]=1
        return con_ind_mat, dis_ind_mat, rank_ind_mat
        
    def _get_threshold(self,con_mat,dis_mat):
        c_bar=0;
        d_bar=0;
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if r!=c:
                    c_bar+=con_mat[r,c]
                    d_bar+=dis_mat[r,c]
        c_bar=c_bar/(self.NUM_ALTS*(self.NUM_ALTS-1))
        d_bar=d_bar/(self.NUM_ALTS*(self.NUM_ALTS-1))
        return c_bar, d_bar

    def plot_graph(self):
        color=['r','g','b','c','m','y','k']
        ax=plt.gca()
        ax.set_title("Alternative Scores")
        ax.set_xticks(list(range(0,len(self.ATBS))),labels=self.ATBS)
        for i in range(len(self.ALTS)):
            plt.plot(self.SURVEY[i,:],marker=".",markersize=15,color=color[i%7],label=self.ALTS[i])

        ax.legend(self.ALTS,loc="upper right")
        plt.show()
    def _Interprete(self,rank_ind_mat):
        self._txtResult.append("Outrank results \n")
        for r in range(self.NUM_ALTS):
            for c in range(self.NUM_ALTS):
                if rank_ind_mat[r,c]==1:
                    self._txtResult.append(f"{self.ALTS[r]} outrank {self.ALTS[c]} \n")
                    
        
    def _Close(self):      
        self.close()
        QApplication.quit()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=frmELECTRE()
    sys.exit(app.exec_())
    
    
    
    

