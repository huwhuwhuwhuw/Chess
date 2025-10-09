#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 15:55:47 2025

@author: huwtebbutt
"""

def Check_Pawn(self,Target_Piece,PX,PY,TX,TY,Move_List):
    
    #Check moving forward 1 space
    if PX==TX and abs(PY-TY)==1:
        #Pawn is moving forward one space
        #Check moving right direction
        if (TY-PY==1 and self.Turn=="White") or (TY-PY==-1 and self.Turn=="Black"):
            #Check square is empty
            if Target_Piece == self.Empty:
                return True
            else: return False
        else: return False
    #Check moving forward 2 spaces
    elif PX==TX and abs(PY-TY)==2:
        #Check on starting square
        if ((self.Turn=="White" and PY-self.Down_Border==1) 
            or (self.Turn=="Black" and self.Y_Size==PY+self.Up_Border+2)):
            #Check squares are empty
            try:
                Middle_Square=self.Board[TX][int((TY+PY)/2)]
            except IndexError:
                Middle_Square=self.Empty
            if Target_Piece == Middle_Square == self.Empty:
                return True
            else: return False
        else: return False
    #Check Capturing
    elif abs(TY-PY)==1 and abs(TX-PX)==1:
        #Pawn is attempting to capture
        if Target_Piece != self.Empty:
            #Piece can capture
            return True
        #Check empassant (STUPID FUCKING RULE)
        else:
            #Define variables for convenience
            Prev_Move=Move_List[-1]
            Prev_Piece=Prev_Move[0]
            Prev_PXPY=Prev_Move[1]
            Prev_TXTY=Prev_Move[2]
            #Check prev piece to move was a pawn
            if Prev_Piece.upper() != 'P':
                return False
            #moved two spaces
            if abs(Prev_PXPY[1]-Prev_TXTY[1])!=2:
                return False
            #and is in the correct position to enpassant
            if Prev_TXTY[0]!=TX and Prev_TXTY[1]!=PY:
                return False
            #If all conditions met, enpassant is possible
            return True
    else: return False