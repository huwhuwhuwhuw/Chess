#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 15:56:17 2025

@author: huwtebbutt
"""

def Update_Bounds(self,Piece,Piece_Coords,Target_Coords):
    from numpy import delete,vstack,hstack,array
    
    #Change board
    PX=Piece_Coords[0]
    PY=Piece_Coords[1]
    TX=Target_Coords[0]
    TY=Target_Coords[1]
    Vector_X=TX-PX
    Vector_Y=TY-PY
    
    #Create temporary copies of variables
    New_Left_Border=self.Left_Border -Vector_X
    New_Right_Border=self.Right_Border +Vector_X
    New_Down_Border=self.Down_Border  -Vector_Y
    New_Up_Border=self.Up_Border    +Vector_Y
    
    New_White_King_Coords=[None,None]
    New_White_King_Coords[0]=self.White_King_Coords[0]-Vector_X
    New_White_King_Coords[1]=self.White_King_Coords[1]-Vector_Y
    New_Black_King_Coords=[None,None]
    New_Black_King_Coords[0]=self.Black_King_Coords[0]-Vector_X
    New_Black_King_Coords[1]=self.Black_King_Coords[1]-Vector_Y
    
    #Create copy of board
    New_Board=self.Board.copy()
    
    
    #Remove current Piece
    New_Board[PX][PY]=self.Empty
    #Check stupid fucking enpassant
    if Piece=='P' or Piece=='p':
        if PX!=TX and New_Board[TX][TY]==self.Empty:
            print("ENPASSANTING\n"*3)
            New_Board[TX][PY]=self.Empty
    
    
    
    if Vector_X>0:
        List=list(range(Vector_X))
        New_Board=delete(New_Board,List,axis=0)
        for i in range(Vector_X):
            New_Board=vstack([New_Board,array([self.Empty]*self.Y_Size)])
            
    elif Vector_X<0:
        List=[-(a+1) for a in range(-Vector_X)]
        New_Board=delete(New_Board,List,axis=0)
        for i in range(abs(Vector_X)):
            New_Board=vstack([array([self.Empty]*self.Y_Size),New_Board])
    
    if Vector_Y>0:
        print(f"Before Delete {New_Board.shape}")
        List=list(range(Vector_Y))
        New_Board=delete(New_Board,List,axis=1)
        print(f"AFter Delete {New_Board.shape}")
        for i in range(Vector_Y):
            New_Board=hstack([New_Board, array([[self.Empty]]*self.X_Size)])
    elif Vector_Y<0:
        List=[-(a+1) for a in range(-Vector_Y)]
        New_Board=delete(New_Board,List,axis=1)
        for i in range(abs(Vector_Y)):
            New_Board=hstack([array([[self.Empty]]*self.X_Size),New_Board])
        
    #Replace Piece
    New_Board[PX][PY]=Piece
    Attrs=[New_White_King_Coords,New_Black_King_Coords,
           New_Left_Border,New_Right_Border,
           New_Up_Border,New_Down_Border]
    return New_Board,Attrs





