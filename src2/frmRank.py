#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:08:34 2024

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
from SAW import *
from TOPSIS import *
from ELECTRE import *
class frmRank(QWidget):
    def __init__(self,**kwargs):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        self.norm_obj=kwargs['norm_obj']
        
        self.ALTS=self.norm_obj['ALTS']
        self.NUM_ALTS=self.norm_obj['NUM_ALTS']
        
        self.ATBS=self.norm_obj['ATBS']
        self.NUM_ATBS=self.norm_obj['NUM_ATBS']
        self.WEIGHTS=self.norm_obj['WEIGHTS']
        self.RAW_SURVEY=self.norm_obj['RAW_SURVEY']
        self.RAW_PROP=self.norm_obj['RAW_PROP']
        self.ATB_PROP=self.norm_obj['ATB_PROP']
        self.NORM_MATRIX=self.norm_obj['NORM_MATRIX']
        self.WNORM_MATRIX=self.norm_obj['WNORM_MATRIX']
        
        self._add_widget('_lblTitle',QLabel('RANK',self),[0,0,1,6])     
        self._add_widget('_lblSelection',QLabel('RANK Method',self),[6,0,1,2])
        self._add_widget('_cmbSelections',QComboBox(self),[6,2,1,4])
        self._cmbSelections.addItems(['[0]: SAW','[1]: TOPSIC','[2]: ELECTRE'])
        self._cmbSelections.setEditable(False)
        
       
       
        self._add_widget('_btnRank',QPushButton("Rank",self),[7,2,1,1],func=self._Rank)
        self._add_widget('_btnClear',QPushButton("Clear",self),[7,3,1,1],func=self._Clear)
        self._add_widget('_btnSave',QPushButton("Save",self),[7,4,1,1],func=self._Save)
        self._add_widget('_btnClose',QPushButton("Close",self),[7,5,1,1],func=self._Close)
        self._add_widget('_txtResult',QTextEdit('',self),[8,0,10,6])  
       
       
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
        
    def _Rank(self):
        ind=self._cmbSelections.currentIndex()
        if ind==0:
            self._SAW=SAW(norm_obj=self.norm_obj,board=self._txtResult)
            self._SAW.Rank()
        if ind==1:
            self._TOPSIS=TOPSIS(norm_obj=self.norm_obj,board=self._txtResult)
            self._TOPSIS.Rank()
        if ind==2:
            self._ELECTRE=ELECTRE(norm_obj=self.norm_obj,board=self._txtResult)
            self._ELECTRE.Rank()
            
    def _Save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 
           "Save File", "", "All Files(*);;Text Files(*.txt)", options = options)
        if fileName:
            with open(fileName, 'w') as f:
                f.write(self._txtResult.toPlainText())
    
    
    def _Close(self):      
        self.close()
        QApplication.quit()
        
   
    
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
        
