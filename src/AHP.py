#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 09:20:16 2024

@author: kyphuc
"""

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

class frmAHP(QWidget):
    def __init__(self,**kwargs):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        
        self._add_widget('_lblTitle',QLabel('AHP ONE TABLE METHOD',self),[0,0,1,6])     
        self._add_widget('_lblParentsName',QLabel('Parent Name',self),[1,0,1,2])    
        self._add_widget('_txtParentsName',QLineEdit('',self),[1,2,1,4])  
        self._add_widget('_lblParentsWeight',QLabel('Parent Weight',self),[2,0,1,2])
        self._add_widget('_txtParentsWeight',QLineEdit('',self),[2,2,1,4])  
        self._add_widget('_lblAlternatives',QLabel('Input list of alternatives',self),[3,0,1,2])
        self._add_widget('_txtAlternatives',QLineEdit('',self),[3,2,1,4])  
        
        self._add_widget('_btnRun',QPushButton("Run",self),[6,3,1,1],func=self._Run)
        self._add_widget('_btnSave',QPushButton("Save",self),[6,4,1,1],func=self._SaveResult)
        self._add_widget('_btnClose',QPushButton("Close",self),[6,5,1,1],func=self._Close)
        self._add_widget('_txtResult',QTextEdit('',self),[7,0,10,6])  
       
       
        
        self._lblTitle.setFont(QFont("Times",20, QFont.Bold))
        self._lblTitle.setStyleSheet("color: blue")
        self._lblTitle.setAlignment(Qt.AlignCenter)
        self._layout.setVerticalSpacing(10)
        self._layout.setHorizontalSpacing(10)
        self.setWindowTitle('AHP 1 TABLE')        
        self.setLayout(self._layout)
        self.setFixedSize(600,500)
        
        #self.openDatabase()
        self.setWindowState(Qt.WindowActive)
        self.show()
        
        self.PARENTS=None
        self.PARENTS_WEIGHT=0
        self.ALTS=None
        self.NUM_ALTS=0
        self.WEIGHTS=None
        self.SURVEY=None
        
    def _add_widget(self,comp,item,pos,**kwargs):
        self .__setattr__(comp,item) 
        self._layout.addWidget(getattr(self,comp),pos[0],pos[1],pos[2],pos[3])
        if 'func' in kwargs:
            getattr(self,comp).clicked.connect(kwargs['func'])   
            
    def _Run(self):
        self._GetData()
        
        self._AHP()
        
    def _SaveResult(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 
            "Save File", "", "All Files(*);;Text Files(*.txt)", options = options)
        if fileName:
            with open(fileName, 'w') as f:
                f.write(self._txtResult.toPlainText())
                 
    def _GetData(self):
        self.PARENTS=self._txtParentsName.text()
        self.PARENTS_WEIGHT=float(self._txtParentsWeight.text())
        self.ALTS=self._txtAlternatives.text().split(',')
        self.NUM_ALTS=len(self.ALTS)
        print("num alts",self.NUM_ALTS)
        print(self.ALTS)
        
        self.SURVEY=np.eye(self.NUM_ALTS)
        for r in range(self.NUM_ALTS):
            for c in range(r+1,self.NUM_ALTS):      
                while True:
                    str_text,ok =QInputDialog.getText(self,"Get input",f"How many times you prefer {self.ALTS[r]} to {self.ALTS[c]} : ")
                    if ok and len(str_text) > 0:
                        break
                str_lst=eval(str_text)
                self.SURVEY[r,c]= str_lst
                self.SURVEY[c,r]=1/self.SURVEY[r,c]
        
        
    def _AHP(self):
        self._txtResult.clear()
        self._txtResult.append("AHP Method Report \n")
        self._txtResult.append("Parents: \n"+str(self.PARENTS) + "\n")
        self._txtResult.append("Parents Weight: \n" + str(self.PARENTS_WEIGHT) + "\n")
        self._txtResult.append("Alternatives: \n" +str(self.ALTS) + "\n")
        self._txtResult.append("The survey matrix: \n" + str(self.SURVEY) +"\n")
      
        col_sum,new_mat=self.normalize()
        self._txtResult.append("The column sum: \n" + str(col_sum) +"\n")
        self._txtResult.append("The normalize matrix: \n" + str(new_mat) +"\n")
      
        eig_vals,lambda_max,w_priority=self._get_eig(new_mat)
       
        self._txtResult.append("The eigen value: \n" + str(eig_vals) +"\n")
        self._txtResult.append("The lambda max: \n" + str(lambda_max) +"\n")
        self._txtResult.append("The w priority: \n" + str(w_priority) +"\n")
        
        CI,CR,con=self._check_CI(lambda_max)
        self._txtResult.append("The CI: \n" + str(CI) +"\n")
        self._txtResult.append("The CR: \n" + str(CR) +"\n")
        self._txtResult.append("The Results are: \n" + str(con) +"\n")
    def normalize(self):
        col_sum=np.sum(self.SURVEY,axis=(0))
        new_mat=np.zeros((self.NUM_ALTS,self.NUM_ALTS))
        for i in range(self.NUM_ALTS):
            for j in range(self.NUM_ALTS):
                new_mat[i][j]=self.SURVEY[i][j]/col_sum[j]
        return col_sum, new_mat
    
    def _get_eig(self,mat):
        eig_vals=1/self.NUM_ALTS*np.sum(mat,axis=(1))
        col_sum=np.sum(self.SURVEY,axis=(0))
        lambda_max=np.dot(eig_vals,col_sum)
        w_priority=self.PARENTS_WEIGHT*eig_vals
        return eig_vals, lambda_max, w_priority
    def _check_CI(self,lambda_max):
        CI=(lambda_max-self.NUM_ALTS)/(self.NUM_ALTS-1)
        RI=[0,0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49]
        CR=CI/RI[self.NUM_ALTS]
        
        if CR <= 0.1:
            con="Quite Consistent"
        else:
            con="Inconsistent"
        return CI, CR, con
    def _Close(self):      
        self.close()
        #QApplication.quit()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=frmAHP()
    sys.exit(app.exec_())