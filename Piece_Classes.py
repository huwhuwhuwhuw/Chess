#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 12:46:53 2025

@author: huwtebbutt
"""

class Piece:
    def __init__(self, x, y, name, colour):
        self.x=x
        self.y=y
        self.Colour=colour
        self.Name=name
        self.Has_Moved=False
        self.Castling=False
        self.EnPassanting=False
        self.Attacking_King=False
    
    def __str__(self):
        if self.Name!='Empty':
            return f"{self.Colour[0]}{self.Name[0]}"
        else: return '_'
    
    def display(self):
        if self.Colour=="White":
            return self.Name[0]
        elif self.Colour=='Black':
            return self.Name[0].lower()
        else:
            return "_"
        
    def __eq__(self,other):
        if type(other)==str:
            if other == self.Name:
                return True
            else:
                return False
        else:
            if type(other)==Rook and self.Name=='Rook':
                return True
            elif type(other)==Horse and self.Name=='Horse':
                return True
            elif type(other)==Bishop and self.Name=='Bishop':
                return True
            elif type(other)==Queen and self.Name=='Queen':
                return True
            elif type(other)==King and self.Name=='King':
                return True
            elif type(other)==Pawn and self.Name=='Pawn':
                return True
            elif type(other)==Empty and self.Name=='Empty':
                return True
            else:
                return False
            
    
    def coords(self):
        return self.x,self.y
    def update_coords(self,x,y):
        self.x=x
        self.y=y
    def update_coords_relative(self,x,y):
        self.x+=x
        self.y+=y
    
    
    def is_Right_Turn(self,Turn):
        if Turn==self.Colour:
            return True
        else: return False
    
    def is_Friendly_Fire(self,Target_Piece):
        if self.Colour == Target_Piece.Colour:
            return True
        else: return False
    
    def General_legal(self,Board,TX,TY):
        if self.x == TX and self.y == TY: #Piece hasnt moved
            print("Im not seeing enough movement")
            return False
        
        if not self.is_Right_Turn(Board.Turn): #Player is moving opponents piece
            print("Wrong turn")
            return False
        
        if Board.get_Piece(TX,TY) != 'Empty' and self.is_Friendly_Fire(Board.get_Piece(TX,TY)):
            #Player is capturing their own piece
            print("Friendly Fire")
            return False
        return True
    def is_Being_Attacked(self,Board):
        #Define Movment Functions
        def Up_Func(x):
            return x+1
        def Down_Func(x):
            return x-1
        def Still_Func(x):
            return x
        Move_Set=[[Up_Func,Still_Func],
                  [Down_Func,Still_Func],
                  [Still_Func,Up_Func],
                  [Still_Func,Down_Func],
                  [Up_Func,Up_Func],
                  [Up_Func,Down_Func],
                  [Down_Func,Up_Func],
                  [Down_Func,Down_Func]]
        #Check each movement option for queen,rooks and bishops
        for x_func,y_func in Move_Set:
            x=self.x
            y=self.y
            Square='Empty'
            while Square=='Empty':
                Diagonal=False
                Hori_Verti=False
                x=x_func(x)
                y=y_func(y)
                if x!=x_func(x) and y!=y_func(y):
                    Diagonal = True
                else:
                    Hori_Verti=True
                if x<0 or y<0 or x>Board.X_Size or y>Board.Y_Size:
                    break
                Square=Board.get_Piece(x,y)
                if Square=="Queen" and Square.Colour != Board.Turn:
                    return True
                elif Square=="Bishop" and Square.Colour != Board.Turn and Diagonal==True:
                    return True
                elif Square=="Rook" and Square.Colour != Board.Turn and Hori_Verti==True:
                    return True
        #Create move set for horsey
        Moves=[[1,2],[1,-2],[-1,2],[-1,-2],
               [2,1],[2,-1],[-2,1],[-2,-1]]
        #Check each square for a horse
        for Move in Moves:
            Square=Board.get_Piece(self.x+Move[0],self.y+Move[1])
            if Square == 'Horse' and Square.Colour != Board.Turn:
                return True
        #Check squares adjacent for kings and pawns
        Move_List=[[1,0],
                   [1,1],
                   [1,-1],
                   [-1,0],
                   [-1,1],
                   [-1,-1],
                   [0,1],
                   [0,-1]]
        for Move in Move_List:
            Square=Board.get_Piece(self.x+Move[0],self.y+Move[1])
            if Square=='King' and Square.Colour!=self.Colour:
                return True
            elif Square=='Pawn' and Square.Colour!=self.Colour:
                #If Black pawn, it must be above the square and on the diagonal
                if Square.Colour=="Black" and self.x!=self.x+Move[0] and self.y+Move[1]-self.y>0:
                    return True
                #If white pawn, it must be below the square and on the diagonal
                elif Square.Colour=="White" and self.x!=self.x+Move[0] and self.y+Move[1]-self.y<0:
                    return True
        return False

class Pawn(Piece):
    def is_legal_move(self,Board,TX,TY):
        PX=self.x
        PY=self.y
        
        if not self.General_legal(Board,TX,TY):
            return False
        Target_Piece=Board.get_Piece(TX,TY)
        
        #Check all possible pawn moves are correct
        #Check moving 1 space
        if PX==TX and abs(PY-TY)==1:
            #Pawn is moving forward one space
            #Check moving right direction
            if (TY-PY==1 and Board.Turn=="White") or (TY-PY==-1 and Board.Turn=="Black"):
                #Check square is empty
                if Target_Piece == 'Empty':
                    return True
                else: return False
            else: return False
        
        #Check moving 2 spaces
        elif PX==TX and abs(PY-TY)==2:
            #Check on starting square
            if not self.Has_Moved:
                #Check squares are empty
                Middle_Square=Board.get_Piece(TX,int((TY+PY)/2))
                if Target_Piece == 'Empty' and Middle_Square == 'Empty':
                    return True
                else: return False
            else: return False
        
        #Check Capturing
        elif abs(TY-PY)==1 and abs(TX-PX)==1:
            #Pawn is attempting to capture
            if Target_Piece != 'Empty':
                #Piece can capture
                return True
            
            else: #Target is empty, Check empassant
                Move_List=Board.Move_List
                #Define variables for convenience
                Prev_Move=Move_List[-1]
                Prev_Piece=Prev_Move[0]
                Prev_PXPY=Prev_Move[1]
                Prev_TXTY=Prev_Move[2]
                #Make sure prev piece to move was a pawn
                if Prev_Piece != 'Pawn':
                    return False
                #it moved two spaces
                if abs(Prev_PXPY[1]-Prev_TXTY[1])!=2:
                    return False
                #and is in the correct position to enpassant
                if Prev_TXTY[0]!=TX and Prev_TXTY[1]!=PY:
                    return False
                #If all conditions met, enpassant is possible
                self.EnPassanting=True
                return True
        else: return False
    
    def is_Attacking_King(self,Board):
        if self.Colour=='White':
            Square_1=Board.get_Piece(self.x+1,self.y-1)
            Square_2=Board.get_Piece(self.x+1,self.y+1)
            if Square_1 =='King' and Square_1.Colour=='Black':
                return True
            elif Square_2 =='King' and Square_2.Colour=='Black':
                return True
            else: return False
        elif self.Colour=='Black':
            Square_1=Board.get_Piece(self.x-1,self.y-1)
            Square_2=Board.get_Piece(self.x-1,self.y+1)
            if Square_1 =='King' and Square_1.Colour=='White':
                return True
            elif Square_2 =='King' and Square_2.Colour=='White':
                return True
            else: return False
        else: return False

class Horse(Piece):
    def is_legal_move(self,Board,TX,TY):
        PX=self.x
        PY=self.y
        if not self.General_legal(Board,TX,TY):
            return False
        
        #Check L-shape movement
        if (abs(TX-PX)==1 and abs(TY-PY)==2) or (abs(TX-PX)==2 and abs(TY-PY)==1):
            return True
        else: 
            return False
    
    def is_Attacking_King(self,Board):
        Moves=[[1,2],[1,-2],[-1,2],[-1,-2],
               [2,1],[2,-1],[-2,1],[-2,-1]]
        for Move in Moves:
            Square=Board.get_Piece(self.x+Move[0],self.y+Move[1])
            if Square == 'King' and Square.Colour != self.Colour:
                return True
            else: return False

class Bishop(Piece):
    def is_legal_move(self,Board,TX,TY):
        PX=self.x
        PY=self.y
        
        if not self.General_legal(Board,TX,TY):
            return False
        
        from numpy import linspace
        #Check bishop is moving diagonally
        if (PX==TX or PY==TY) or (abs(TY-PY) != abs(TX-PX)):
            #Not moving diagonally
            return False
        else:
            #Check all inbetween squares are empty
            for i,(X,Y) in enumerate(zip(linspace(PX,TX,abs(TX-PX)+1),linspace(PY,TY,abs(TY-PY)+1))):
                X=int(X)
                Y=int(Y)
                #Ignore starting and target square
                if i==0 or (X==TX and Y==TY):
                    continue
                if Board.get_Piece(X,Y) != 'Empty':
                    return False
        return True
    
    def is_Attacking_King(self,Board):
        #Define Movment Functions
        def Up_Func(x):
            return x+1
        def Down_Func(x):
            return x-1
        #Bishop can move in the four diagonals
        Move_Set=[[Up_Func,Up_Func],
                  [Up_Func,Down_Func],
                  [Down_Func,Up_Func],
                  [Down_Func,Down_Func]]
        #Check each diagonal for a piece
        for x_func,y_func in Move_Set:
            x=self.x
            y=self.y
            Square='Empty'
            while Square=='Empty':
                x=x_func(x)
                y=y_func(y)
                if x<0 or y<0 or x>Board.X_Size or y>Board.Y_Size:
                    break
                Square=Board.get_Piece(x,y)
                if Square=='King' and Square.Colour != self.Colour:
                    return True
        return False

class Rook(Piece):
    def is_legal_move(self,Board,TX,TY):
        PX=self.x
        PY=self.y
        
        if not self.General_legal(Board,TX,TY):
            return False
        
        from numpy import linspace
        #Check where it is moving
        if PX!=TX and PY!=TY:
            #Moving Diagonally
            return False
        Amount_of_Squares=max(abs(TX-PX)+1,abs(TY-PY)+1)
        for i,(X,Y) in enumerate(zip(linspace(PX,TX,Amount_of_Squares),linspace(PY,TY,Amount_of_Squares))):
            X=int(X)
            Y=int(Y)
            #Ignore starting and target squares
            if i==0 or (X==TX and Y==TY):
                continue
            if Board.get_Piece(X,Y) != 'Empty':
                return False
        return True
    
    def is_Attacking_King(self,Board):
        #Define Movment Functions
        def Up_Func(x):
            return x+1
        def Down_Func(x):
            return x-1
        def Still_Func(x):
            return x
        #Rook can move in the four cardinal directions
        Move_Set=[[Up_Func,Still_Func],
                  [Down_Func,Still_Func],
                  [Still_Func,Up_Func],
                  [Still_Func,Down_Func]]
        #Check each diagonal for a piece
        for x_func,y_func in Move_Set:
            x=self.x
            y=self.y
            Square='Empty'
            while Square=='Empty':
                x=x_func(x)
                y=y_func(y)
                if x<0 or y<0 or x>Board.X_Size or y>Board.Y_Size:
                    break
                Square=Board.get_Piece(x,y)
                if Square=='King' and Square.Colour != self.Colour:
                    return True
        return False

class Queen(Piece):
    def is_legal_move(self,Board,TX,TY):
        PX=self.x
        PY=self.y
        
        if not self.General_legal(Board,TX,TY):
            print("General Legal")
            return False
        
        #Check movement
        if (TX-PX!=0 and TY-PY!=0):
            #Not horizontal
            if abs(TX-PX) != abs(TY-PY):
                #Not Diagonal
                print("Issue with diagonal")
                return False
            
        from numpy import linspace
        Amount_of_Squares=max(abs(TX-PX)+1,abs(TY-PY)+1)
        for i,(X,Y) in enumerate(zip(linspace(PX,TX,Amount_of_Squares),linspace(PY,TY,Amount_of_Squares))):
            X=int(X)
            Y=int(Y)
            #Ignore starting and target squares
            if i==0 or (X==TX and Y==TY):
                continue
            elif Board.get_Piece(X,Y) != 'Empty':
                print("Not empty square?")
                return False
        return True
    
    def is_Attacking_King(self,Board):
        #Define Movment Functions
        def Up_Func(x):
            return x+1
        def Down_Func(x):
            return x-1
        def Still_Func(x):
            return x
        #Queen can move in the four diagonals + four cardinal directions
        Move_Set=[[Up_Func,Still_Func],
                  [Down_Func,Still_Func],
                  [Still_Func,Up_Func],
                  [Still_Func,Down_Func],
                  [Up_Func,Up_Func],
                  [Up_Func,Down_Func],
                  [Down_Func,Up_Func],
                  [Down_Func,Down_Func]]
        #Check each movement option for a piece
        for x_func,y_func in Move_Set:
            x=self.x
            y=self.y
            Square='Empty'
            while Square=='Empty':
                x=x_func(x)
                y=y_func(y)
                if x<0 or y<0 or x>Board.X_Size or y>Board.Y_Size:
                    break
                Square=Board.get_Piece(x,y)
                if Square=='King' and Square.Colour != self.Colour:
                    return True
        return False
    
class King(Piece):
    def is_legal_move(self,Board,TX,TY):
        PX=self.x
        PY=self.y
        
        if not self.General_legal(Board,TX,TY):
            return False
        if abs(PY-TY)>1:
            return False
        if abs(PX-TX)>1:
            #Check castling
            if abs(PX-TX)!=2:
                return False
            if self.Has_Moved:
                return False
            #In the direction of movement, check if there is a rook which has not moved
            x=int((TX-PX)/abs(TX-PX))

            while True:
                PX+=x
                if PX>Board.X_Size or PX<0:
                    return False
                
                Square=Board.get_Piece(PX,PY)
                if Square=='Empty':
                    continue
                elif Square=='Rook' and Square.Has_Moved==False and Square.Colour==self.Colour:
                    self.Castling=True
                    return True
                else:
                    return False
                
            
        return True
    
    def is_Attacking_King(self,Board):
        Move_List=[[1,0],
                   [1,1],
                   [1,-1],
                   [-1,0],
                   [-1,1],
                   [-1,-1],
                   [0,1],
                   [0,-1]
                   ]
        for Move in Move_List:
            Square=Board.get_Piece(self.x+Move[0],self.y+Move[1])
            if Square=='King' and Square.Colour!=self.Colour:
                return True
        return False

class Empty(Piece):
    def is_Attacking_King(self,Board):
        return False
