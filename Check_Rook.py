#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 16:09:28 2025

@author: huwtebbutt
"""

def Check_Rook(self,PX,PY,TX,TY):
    from numpy import linspace
    #Check where its moving
    if PX!=TX and PY!=TY:
        #Moving Diagonally
        return False
    if PX!=TX:
        #Moving Horizontally
        #Check all squares are empty
        for i,X in enumerate(linspace(PX,TX,abs(TX-PX)+1)):
            #Ignore starting square and squares that are out of bounds
            if i==0 or X==TX or X<0 or X>self.X_Size-1:
                continue
            if self.Board[int(X)][TY] != self.Empty:
                return False
        
    elif PY!=TY:
        #Moving Vertically
        #Check all squares are empty
        for i,Y in enumerate(linspace(PY,TY,abs(TY-PY)+1)):
            #Ignore starting square and squares that are out of bounds
            if i==0 or Y==TY or Y<0 or Y>self.Y_Size-1:
                continue
            if self.Board[TX][int(Y)] != self.Empty:
                return False
    return True