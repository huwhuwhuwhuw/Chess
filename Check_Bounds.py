#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 14:30:56 2025

@author: huwtebbutt
"""

def Check_Bounds(self,Piece_Coords,Target_Coords):
    PX=Piece_Coords[0]
    PY=Piece_Coords[1]
    TX=Target_Coords[0]
    TY=Target_Coords[1]
    Vector_X=TX-PX
    Vector_Y=TY-PY
    
    for i,row in enumerate(self.Board):
        for j,square in enumerate(row):
            if i==TX and j==TY:
                continue
            if square!=self.Empty:
                if i-Vector_X<0 or j-Vector_Y<0:
                    return False
                try:
                    self.Board[i-Vector_X][j-Vector_Y]
                except IndexError:
                    return False
    return True