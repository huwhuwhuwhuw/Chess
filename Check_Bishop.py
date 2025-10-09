#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 13:25:51 2025

@author: huwtebbutt
"""

def Check_Bishop(self,PX,PY,TX,TY):
    from numpy import linspace
    #Check bishop is moving diagonally
    if (PX==TX or PY==TY) or (abs(TY-PY) != abs(TX-PX)):
        #Not moving diagonally
        return False
    else:
        #Check all squares are empty
        for i,(X,Y) in enumerate(zip(linspace(PX,TX,abs(TX-PX)+1),linspace(PY,TY,abs(TY-PY)+1))):
            if i==0 or X==TX or X>self.X_Size-1 or Y>self.Y_Size-1 or X<0 or Y<0:
                continue
            if self.Board[int(X)][int(Y)] != self.Empty:
                return False
    return True