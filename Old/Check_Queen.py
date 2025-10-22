#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 13:34:41 2025

@author: huwtebbutt
"""

def Check_Queen(self,PX,PY,TX,TY):
    from numpy import linspace
    
    if TX != PX and TY == PY:
        #Moving Horizontally
        for i,X in enumerate(linspace(PX,TX,abs(TX-PX)+1)):
            if i==0 or X==TX:
                continue
            if self.Board[int(X)][TY] != self.Empty:
                return False
    elif TX == PX and TY != PY:
        #Moving Vertically
        for i,Y in enumerate(linspace(PY,TY,abs(TY-PY)+1)):
            if i==0 or Y==TY:
                continue
            if self.Board[TX][int(Y)] != self.Empty:
                return False
    elif TX != PX and TY != PY:
        #Moving Diagonally
        if abs(TY-PY) != abs(TX-PX):
            #Not straight diagonal
            return False
        for i,(X,Y) in enumerate(zip(linspace(PX,TX,abs(TX-PX)+1),linspace(PY,TY,abs(TY-PY)+1))):
            if i==0 or X==TX:
                continue
            if self.Board[int(X)][int(Y)] != self.Empty:
                return False
    return True
