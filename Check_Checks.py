#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 21:21:27 2025

@author: huwtebbutt
"""

def Check_Checks(self,Board,WKC,BKC):
    def Up_Func(x):
        return x+1
    def Down_Func(x):
        return x-1
    def Still_Func(x):
        return x
    
    def Check_Squares(X_Func,X,Y_Func,Y,Danger_Pieces):
        i=0
        while True:
            i+1
            X=X_Func(X)
            Y=Y_Func(Y)
            if X<0 or Y<0:
                return True
            try:
                Square=Board[X][Y]
            except IndexError:
                #Checked all the squares in this direction
                return True
            if Square!=self.Empty:
                #We have found a piece
                #Check piece colour
                if (Square.isupper() and self.Turn=="White") or (Square.islower() and self.Turn=="Black"):
                    #Piece is same colour, so no danger in this direction
                    return True
                else:
                    #Piece is of opposing colour, check if can hit us
                    if Square.upper() in Danger_Pieces:
                        if Square.upper()=='K':
                            if i>1:
                                return True
                            else:
                                #We have moved into a king
                                return False
                        else:
                            #We have moved into (or failed to prevent) a Queen or rook or bishop
                            return False
                    else:
                        #Piece is not dangerous
                        return True
        return True
    
    if self.Turn=="White":
        White_King_Coords=WKC
        X=White_King_Coords[0]
        Y=White_King_Coords[1]
    else:
        Black_King_Coords=BKC
        X=Black_King_Coords[0]
        Y=Black_King_Coords[1]
    #Check for pawns
    if (((Board[X-1][Y+1]=='p' or Board[X+1][Y+1]=='p') and self.Turn=="White")
        or ((Board[X-1][Y-1]=='P' or Board[X+1][Y-1]=='P') and self.Turn=="Black")):
        return False
    
    #Check Horseys
    H_Coords=[]
    H_Coords.append([X+2,Y+1])
    H_Coords.append([X+2,Y-1])
    H_Coords.append([X-2,Y+1])
    H_Coords.append([X-2,Y-1])
    H_Coords.append([X+1,Y+2])
    H_Coords.append([X+1,Y-2])
    H_Coords.append([X-1,Y+2])
    H_Coords.append([X-1,Y-2])
    for HX,HY in H_Coords:
        if ((Board[HX][HY]=='h' and self.Turn=="White") 
            or (Board[HX][HY]=='H' and self.Turn=="Black")):
            return False
    #Check squares above,below,right,left
    if not Check_Squares(Still_Func,X,Up_Func,Y,['K','Q','R']):
        return False
    if not Check_Squares(Still_Func,X,Down_Func,Y,['K','Q','R']):
        return False
    if not Check_Squares(Up_Func,X,Still_Func,Y,['K','Q','R']):
        
        return False
    if not Check_Squares(Down_Func,X,Still_Func,Y,['K','Q','R']):
        return False
    #Check squares diagonally
    if not Check_Squares(Up_Func,X,Up_Func,Y,['K','Q','B']):
        return False
    if not Check_Squares(Up_Func,X,Down_Func,Y,['K','Q','B']):
        return False
    if not Check_Squares(Down_Func,X,Up_Func,Y,['K','Q','B']):
        return False
    if not Check_Squares(Down_Func,X,Down_Func,Y,['K','Q','B']):
        return False
    return True
    
    
        
    
    
    
                