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
from frmNormalize import *

class frmGetInput(QWidget):
    def __init__(self,**kwargs):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        
        self._add_widget('_lblTitle',QLabel('GET INPUT DATA',self),[0,0,1,6])     
        self._add_widget('_lblAlternatives',QLabel('Input list of alternatives',self),[1,0,1,2])
        self._add_widget('_txtAlternatives',QLineEdit('',self),[1,2,1,4])  
        self._add_widget('_lblAttributes',QLabel('Input list of attributes',self),[2,0,1,2])
        self._add_widget('_txtAttributes',QLineEdit('',self),[2,2,1,4])  
        
        self._add_widget('_lblProperties',QLabel('Input list of properties',self),[3,0,1,2])
        self._add_widget('_txtProperties',QLineEdit('',self),[3,2,1,4])  
        
        self._add_widget('_lblWeights',QLabel('Input list of weights',self),[4,0,1,2])
        self._add_widget('_txtWeights',QLineEdit('',self),[4,2,1,4])  
        
       
        self._add_widget('_chkPlot',QCheckBox("PlotGraph",self),[7,0,1,2])
        self._add_widget('_btnGet',QPushButton("Get Input",self),[7,2,1,1],func=self._Get)
        self._add_widget('_btnClear',QPushButton("Clear",self),[7,3,1,1],func=self._Clear)
        self._add_widget('_btnNorm',QPushButton("Send to Norm",self),[7,4,1,1],func=self._SendToNorm)
        self._add_widget('_btnClose',QPushButton("Close",self),[7,5,1,1],func=self._Close)
        self._add_widget('_txtResult',QTextEdit('',self),[8,0,10,6])  
       
       
        
        self._lblTitle.setFont(QFont("Times",20, QFont.Bold))
        self._lblTitle.setStyleSheet("color: blue")
        self._lblTitle.setAlignment(Qt.AlignCenter)
        self._layout.setVerticalSpacing(10)
        self._layout.setHorizontalSpacing(10)
        self.setWindowTitle('Get Ipnut Data')        
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
        
        self.data={}
        
    def _add_widget(self,comp,item,pos,**kwargs):
        self .__setattr__(comp,item) 
        self._layout.addWidget(getattr(self,comp),pos[0],pos[1],pos[2],pos[3])
        if 'func' in kwargs:
            getattr(self,comp).clicked.connect(kwargs['func'])   
    def _Clear(self):
        self._txtResult.clear()
        self.ALTS=None
        self.NUM_ALTS=0
        self.ATBS=None
        self.NUM_ATBS=0
        self.ATB_PROP=None
        self.WEIGHTS=None
        self.SURVEY=None
        self.data.clear()
        
            
    def _Get(self):
        self._GetData()
        self._txtResult.append("Get Data Report \n")
        self._txtResult.append("Alternative list \n"+str(self.ALTS) + "\n")
        self._txtResult.append("Attribute list \n" + str(self.ATBS) + "\n")
        self._txtResult.append("Attribute prop \n" +str(self.ATB_PROP) + "\n")
        self._txtResult.append("Weight list \n" + str(self.WEIGHTS) + "\n")
        self._txtResult.append("The survey matrix \n" + str(self.SURVEY) +"\n")
        
        if self._chkPlot.isChecked():
            self.plot_graph()
            
        
        
    def _SendToNorm(self):
        self.data.clear()
        self.data['ALTS']=self.ALTS
        self.data['NUM_ALTS']=self.NUM_ALTS
        self.data['ATBS']=self.ATBS
        self.data['NUM_ATBS']=self.NUM_ATBS
        self.data['ATB_PROP']=self.ATB_PROP
        self.data['WEIGHTS']=self.WEIGHTS
        self.data['SURVEY']=self.SURVEY
        self.frmNormalize=frmNormalize(data_obj=self.data)
        self.frmNormalize.move(600,2)
        
                 
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
    ex=frmGetInput()
    ex.move(2,2)
    sys.exit(app.exec_())