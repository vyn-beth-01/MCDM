#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 08:34:19 2024

@author: kyphuc
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:37:09 2022

@author: kyphuc
"""
import sys
import time
import os
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from TOPSIC import *
from VIKOR import *
from PROMETHEE import *
from ELECTRE import *
from AHP import *
from SAW import *
def singleton_dec(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@ singleton_dec
class FrmLogin(QWidget):
    
    def __init__(self):
        super(QWidget,self).__init__()  
        self._layout = QGridLayout()
        
        self._add_widget('_lblTitle',QLabel('MCDM illustrations',self),[0,0,1,3])
        self._add_widget('_lblAuthor',QLabel('Lecturer: Kyphuc',self),[1,0,1,3])
        self._add_widget('_lblMethod',QLabel('Select one MCDM method',self),[2,0,1,3])
        self._add_widget('_btnSelect',QPushButton("Select",self),[3,0,1,1],func=self._Select)
        
        self._add_widget('_btnClose',QPushButton("Close",self),[3,2,1,1],func=self._Close)
        
        self._add_widget('_cmbSelections',QComboBox(self),[4,0,1,3])
        self._cmbSelections.addItems(['[0]: SAW','[1]: TOPSIC','[2]: VIKOR','[3]: PROMETHEE','[4]: ELECTRE','[5]: AHP'])
        self._cmbSelections.setEditable(False)
        
        
        self._btnSelect.setVisible(True)
        
        self._lblTitle.setFont(QFont("Times",20, QFont.Bold))
        self._lblTitle.setStyleSheet("color: blue")

        self._lblTitle.setAlignment(Qt.AlignCenter)
        self._layout.setVerticalSpacing(10)
        self._layout.setHorizontalSpacing(10)
        self.setWindowTitle('MCDM class')        
        self.setLayout(self._layout)
        #self.setFixedSize(1000,600)
       
        self.setWindowState(Qt.WindowActive)
        self.show()
        
   
    def _Select(self):
        ind=self._cmbSelections.currentIndex()
        if ind==0:
            self._SAW=frmSAW()
        if ind==1:
            self._TOPSIC=frmTOPSIC()
        if ind==2:
            self._VIKOR=frmVIKOR()
        if ind==3:
            self._PROMETHEE=frmPROMETHEE()
        if ind==4:
            self._ELECTRE=frmELECTRE()
        if ind==5:
            self._AHP=frmAHP()
            
    def _add_widget(self,comp,item,pos,**kwargs):
        self .__setattr__(comp,item) 
        self._layout.addWidget(getattr(self,comp),pos[0],pos[1],pos[2],pos[3])
        if 'func' in kwargs:
            getattr(self,comp).clicked.connect(kwargs['func'])    
    
    def _Close(self):
        
        self.close()
        QApplication.quit()
     
      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=FrmLogin()
    sys.exit(app.exec_())
    