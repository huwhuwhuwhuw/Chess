#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 18:13:51 2025

@author: huwtebbutt
"""

class Board:
    def __init__(self,Sizes_Y=[5,5],Sizes_X=[5,5]):
        X_Size=Sizes_X[0]+Sizes_X[1]+8
        Y_Size=Sizes_Y[0]+Sizes_Y[1]+8
        self.X_Size=X_Size
        self.Y_Size=Y_Size
        self.Left_Border = Sizes_X[0]
        self.Right_Border = Sizes_X[1]
        self.Down_Border = Sizes_Y[0]
        self.Up_Border = Sizes_Y[1]
        self.Turn='White'
        self.Check=False
        self.Pieces_Attacking_King=[]
        self.Checkmate=False
        self.Move_List=[]
        
        import numpy as np
        from Piece_Classes import Pawn,Horse,Bishop,Rook,Queen,King,Empty
        self.Empty=Empty
        #Create empty board
        board=np.empty((8,8),dtype=object)
        
        #Fill standard board with pieces and empty squares
        board[0][0]=Rook(0,0,'Rook','White')
        board[1][0]=Horse(1,0,'Horse','White')
        board[2][0]=Bishop(2,0,'Bishop','White')
        board[3][0]=Queen(3,0,'Queen','White')
        board[4][0]=King(4,0,'King','White')
        board[5][0]=Bishop(5,0,'Bishop','White')
        board[6][0]=Horse(6,0,'Horse','White')
        board[7][0]=Rook(7,0,'Rook','White')
        for i in range(8):
            board[i][1]=Pawn(i,1,'Pawn','White')
        
        for i in range(8):
            for j in range(4):
                board[i][j+2]=Empty(i,j+2,'Empty',None)
        
        for i in range(8):
            board[i][6]=Pawn(i,6,'Pawn','Black')
        board[0][7]=Rook(0,7,'Rook','Black')
        board[1][7]=Horse(1,7,'Horse','Black')
        board[2][7]=Bishop(2,7,'Bishop','Black')
        board[3][7]=Queen(3,7,'Queen','Black')
        board[4][7]=King(4,7,'King','Black')
        board[5][7]=Bishop(5,7,'Bishop','Black')
        board[6][7]=Horse(6,7,'Horse','Black')
        board[7][7]=Rook(7,7,'Rook','Black')
        self.Board=board
        
        #Add Down and Up Borders
        for _ in range(self.Down_Border):
            self.Board=self.Add_Row(self.Board,8,Down=True)
            
        for _ in range(self.Up_Border):
            self.Board=self.Add_Row(self.Board,Length=8,Up=True)        
        
        #Add Left and Right Borders
        for _ in range(self.Left_Border):
            self.Board=self.Add_Column(self.Board,Height=self.Y_Size,Left=True)
            
        for _ in range(self.Right_Border):
            self.Board=self.Add_Column(self.Board,self.Y_Size,Right=True)
        
        #Update coords and fill empty borders
        for i,row in enumerate(self.Board):
            for j,square in enumerate(row):
                if square==None:
                    self.Board[i,j]=Empty(i,j,'Empty',None)
                else:
                    square.update_coords_relative(self.Left_Border,self.Down_Border)
        
    def show_board(self):
        #Print current board state with coordinates to display to players
        import numpy as np
        import copy
        newboard=np.flipud(copy.deepcopy(self.Board).T)
        
        for i,row in enumerate(newboard):
            for j,square in enumerate(row):
                newboard[i][j]=square.display()
        print(" "+'_' *(self.X_Size*4-1))
        for i, row in enumerate(newboard):
            print(row,np.array(self.Y_Size-i))
        Coord_row=''
        for i in range(self.X_Size):
            Coord_row+=f" {i+1}".center(4)
        print(" "+"\u203E"*(self.X_Size*4-1))
        print(np.array(Coord_row))
    
    def get_Piece(self,x,y=None):
        #Return piece at given coordinates
        if (type(x)==tuple or type(x)==list) and y==None:
            y=x[1]
            x=x[0]
        
        if x>=0 and y>=0 and x<self.X_Size and y<self.Y_Size:
            return self.Board[x,y]
        else:
            
            return self.Empty(None,None,'Empty',None)
        
    def check_Board_Constraints(self,Piece,x,y):
        #Check all pieces are still on the board given a movement in x and y
        for i,row in enumerate(self.Board):
            for j,square in enumerate(row):
                #Ignore current piece as it is the one that is moving
                if Piece.x==i and Piece.y==j:
                    continue
                if square=='Empty':
                    continue
                New_x = square.x + x
                New_y= square.y + y
                if New_x < 0 or New_y<0 or New_x > self.X_Size-1 or New_y > self.Y_Size-1:
                    #Piece has fallen off the board
                    if Piece.Castling:
                        Piece.Castling=False
                    elif Piece.EnPassanting:
                        Piece.Enpassanting=False
                    return False
        return True
    
    def Update_Board(self,Piece,TX,TY):
        from Piece_Classes import Empty,Queen
        import copy
        New_Board=copy.deepcopy(self.Board)
        
        #Special cases
        #En passant
        if Piece.EnPassanting:
            if self.get_Piece(TX,Piece.y) !='Pawn' and Piece!='Pawn':
                raise ValueError("Incorrect set up to Enpassant")
            New_Board[TX,Piece.y]=Empty(TX,Piece.y,'Empty',None)
        #Castling
        elif Piece.Castling:
            from Piece_Classes import Rook
            if Piece !='King':
                raise ValueError("Castling without king")
            #Find which way king is trying to castle
            Direction=int((TX-Piece.x)/2)
            #Add rook to correct place
            New_Board[Piece.x+Direction,Piece.y]=Rook(Piece.x+Direction,Piece.y,'Rook',Piece.Colour)
            New_Board[Piece.x+Direction,Piece.y].Has_Moved=True
            #If short side castle
            if Direction>0:
                #Short side castle, rook will be 3 squares in Direction
                Target_Rook=self.get_Piece(Piece.x+3*Direction,Piece.y)
                if Target_Rook!='Rook':
                    raise ValueError("Rook is not available to castle")
                New_Board[Piece.x+3*Direction,Piece.y]=Empty(Piece.x+3*Direction,Piece.y,'Empty',None)
            elif Direction<0:
                #Long side castle, rook will be 4 squares in Direction
                Target_Rook=self.get_Piece(Piece.x+4*Direction,Piece.y)
                if Target_Rook!='Rook':
                    raise ValueError("Rook is not available to castle")
                New_Board[Piece.x+4*Direction,Piece.y]=Empty(Piece.x+3*Direction,Piece.y,'Empty',None)
            
        #Remove piece from board, replace later
        New_Board[Piece.x,Piece.y]= Empty(Piece.x,Piece.y,'Empty',None)
        
        Relative_x=Piece.x-TX
        Relative_y=Piece.y-TY
        
        #Delete and add rows/columns
        if Relative_x>0:
            for _ in range(Relative_x):
                New_Board=self.Add_Row(New_Board,self.X_Size,Down=True)
                New_Board=self.Delete_Row(New_Board,Up=True)
        elif Relative_x<0:
            for _ in range(abs(Relative_x)):
                New_Board=self.Add_Row(New_Board,self.X_Size,Up=True)
                New_Board=self.Delete_Row(New_Board,Down=True)
        
        if Relative_y>0:
            for _ in range(Relative_y):
                New_Board=self.Add_Column(New_Board,self.Y_Size,Left=True)
                New_Board=self.Delete_Column(New_Board,Right=True)
        elif Relative_y<0:
            for _ in range(abs(Relative_y)):
                New_Board=self.Add_Column(New_Board,self.Y_Size,Right=True)
                New_Board=self.Delete_Column(New_Board,Left=True)
        
        #Update coords and fill empty borders
        for i,row in enumerate(New_Board):
            for j,square in enumerate(row):
                if square==None:
                    New_Board[i,j]=Empty(i,j,'Empty',None)
                else:
                    square.update_coords_relative(Relative_x,Relative_y)
                    #Promote any pawns on the first and final rows
                    if square=='Pawn':
                        if square.Colour=="White" and j==self.Y_Size-1:
                            square=Queen(i,j,'Queen','White')
                        elif square.Colour=='Black' and j==0:
                            square=Queen(i,j,'Queen','Black')
        
        #Replace piece
        Piece.Castling=False
        Piece.EnPassanting=False
        Piece.Has_Moved=True
        New_Board[Piece.x,Piece.y]=Piece
        return New_Board
        
    def Add_Row(self,Board,Length,Up=False,Down=False):
        import numpy as np
        New_Row=np.empty([1,Length],dtype=object)
        if Up:
            Board=np.vstack([Board,New_Row])
            return Board
        elif Down:
            Board=np.vstack([New_Row,Board])
            return Board
    
    def Delete_Row(self,Board,Up=False,Down=False):
        if Up:
            Board=Board[:-1]
            return Board
        elif Down:
            return Board[1:]
    
    def Add_Column(self,Board,Height,Left=False,Right=False):
        import numpy as np
        New_Row=np.empty([Height,1],dtype=object)
        if Left:
            Board=np.hstack([New_Row,Board])
            return Board
        elif Right:
            Board=np.hstack([Board,New_Row])
            return Board
    
    def Delete_Column(self,Board,Left=False,Right=False):
        import numpy as np
        if Left:
            Board=np.delete(Board,0, axis=1)
            return Board
        if Right:
            Board=np.delete(Board,-1, axis=1)
            return Board
    
    def is_Player_in_Check(self):
        #variable for Opposing player
        self.Check=False
        Current_Player_Check=False
        self.Pieces_Attacking_King=[]
        for Row in self.Board:
            for Square in Row:
                if Square.is_Attacking_King(self):
                    print(f"{Square.Colour} {Square.Name} is attacking king")
                    if Square.Colour!=self.Turn:
                        #Player is in check at the end of their turn
                        Current_Player_Check = True
                    elif Square.Colour==self.Turn:
                        #Opposing player is in check
                        Square.Attacking_King=True
                        self.Pieces_Attacking_King.append(Square)
                        self.Check=True
        return Current_Player_Check
    def find_King(self,Colour):
        for i,row in enumerate(self.Board):
            for j, square in enumerate(row):
                if square == 'King' and square.Colour == Colour:
                    return i,j
    
    def is_Checkmate(self):
        if not self.Check:
            return False
        #Check if king can move out of check
        KX,KY=self.find_King(self.Turn)
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
            Square=self.get_Piece(KX+Move[0],KY+Move[1])
            if Square!='Empty' and Square.Colour!=self.Colour:
                if not Square.is_Being_Attacked(self):
                    return False
        #Check how many pieces are attacking the king
        N_Pieces=len(self.Pieces_Attacking_King)
        if N_Pieces>1:
            #King cannot move out the way and more than one piece cannot be blocked in one move
            return True
        #Check if the attacking piece can be taken
        Piece = self.Pieces_Attacking_King[0]
        PX=Piece.x
        PY=Piece.y
        for row in self.Board:
            for square in row:
                if square=='King' and square.Colour==self.Turn:
                    #King is attempting to capture, but we have already checked if the king can move
                    continue
                if square!='Empty' and square.Colour !=Piece.Colour:
                    if square.is_legal_move(self,PX,PY):
                        return False
        
        #King cannot move and piece cannot be taken
        #Check if another piece can block the check
        if Piece =='Horse' or Piece=='King' or Piece=='Pawn':
            #Cannot block horses, Kings and Pawns attack from one square away
            return True
        else:
            #Piece is a queen, rook or bishop
            #Check if it is more than one square away so can be blocked
            if abs(KX-PX)<=1 and abs(KY-PY)<=1:
                return True
            #Create list of squares to try blocking
            from numpy import linspace
            Amount_of_Squares=max(abs(KX-PX)+1,abs(KY-PY)+1)
            for i,(X,Y) in enumerate(zip(linspace(PX,KX,Amount_of_Squares),linspace(PY,KY,Amount_of_Squares))):
                X=int(X)
                Y=int(Y)
                #Ignore starting and king squares
                if i==0 or (X==KX and Y==KY):
                    continue
                for row in self.Board:
                    for square in row:
                        if square!='Empty' and square.Colour !=Piece.Colour:
                            if square.is_legal_move(self,X,Y):
                                return False
        return True
    
    def Switch_Turn(self):
        if self.Turn=='White':
            self.Turn='Black'
        else:
            self.Turn='White'

if __name__ == "__main__":
    x=[1,1]
    y=[1,1]
    B=Board(x,y)
    B.show_board()
