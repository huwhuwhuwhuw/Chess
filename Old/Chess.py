#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 15:37:10 2025

@author: huwtebbutt
"""

class Chess:
    from numpy import linspace
    def __init__(self,Sizes_X: list=[0,0] , Sizes_Y: list=[0,0]):
        from numpy import array
        #Set up known rows
        W_Pieces_Row=['R', 'H', 'B', 'Q', 'K', 'B', 'H', 'R']
        W_Pawn_Row=['P']*8
        B_Pieces_Row=['r', 'h', 'b', 'q', 'k', 'b', 'h', 'r']
        B_Pawn_Row=['p']*8
        
        
        #Set up sizes
        X_Size=Sizes_X[0]+Sizes_X[1]+8
        Y_Size=Sizes_Y[0]+Sizes_Y[1]+8
        self.X_Size=X_Size
        self.Y_Size=Y_Size
        self.Left_Border = Sizes_X[0]
        self.Right_Border = Sizes_X[1]
        self.Down_Border = Sizes_Y[0]
        self.Up_Border = Sizes_Y[1]
        
        #Set up useful variables
        Empty=' '
        self.Empty=Empty
        self.Move_List=[]
        self.White_King_Coords=[self.Left_Border+4, self.Down_Border]
        self.Black_King_Coords=[self.Left_Border+4, self.Down_Border+7]
        
        #Define Board
        Board=[]
        #Create empty rows for the downwards border
        for _ in range(self.Down_Border):
            Board.append([Empty]*(X_Size))
        #Create white pieces row
        Board.append(
            [Empty]*self.Left_Border+
            W_Pieces_Row+
            [Empty]*self.Right_Border
            )
        #Create white pawn row
        Board.append(
            [Empty]*self.Left_Border+
            W_Pawn_Row+
            [Empty]*self.Right_Border
            )
        #Create space between white and black rows
        for _ in range(4):
            Board.append([Empty]*(X_Size))
        #Create black pawn row
        Board.append(
            [Empty]*self.Left_Border+
            B_Pawn_Row+
            [Empty]*self.Right_Border
            )
        #Create black pieces row
        Board.append(
            [Empty]*self.Left_Border+
            B_Pieces_Row+
            [Empty]*self.Right_Border
            )
        #Create empty rows for upwards border
        for _ in range(self.Up_Border):
            Board.append([Empty]*(X_Size))
        
        #Rotate board so rows are horizontal
        Board=array(Board).T
        self.Board=Board
    
    def Display_Board(self, Coords=False):
        #Print the board
        from numpy import array,flipud
        
        if Coords:
            print(" "+'_' *(self.X_Size*4-1))
            for i, row in enumerate(reversed(self.Board.T)):
                print(row,array(self.Y_Size-i))
            Coord_row=''
            for i in range(self.X_Size):
                Coord_row+=f" {i+1}".center(4)
            print(" "+"\u203E"*(self.X_Size*4-1))
            print(array(Coord_row))
        
        else:
            print(" "+'_' *(self.X_Size*4+1))
            Display_Board=flipud(self.Board.T)
            print(Display_Board)
            print(" "+"\u203E"*(self.X_Size*4+1))
            
    
    
    def Play(self):
        
        def Get_Coords(self):
            #Set up infinite while loop to ask for a move
            #Define a failsafe that breaks loop
            End_of_Move=False
            Failsafe=0
            while End_of_Move==False:
                Failsafe+=1
                if Failsafe >30:
                    raise RuntimeError("Too many illegal moves, consider resigning")
                
                #Set up another while loop to ask for Piece coords
                Got_Piece_Coords=False
                while Got_Piece_Coords==False:
                    Failsafe+=1
                    if Failsafe>30:
                        raise RuntimeError("Too many illegal moves, consider resigning")
                    #Ask for piece coords in format "X Y"
                    Message=f"Input Piece coordinates, Turn={self.Turn}\n(Format: X Y)\n: "
                    Piece_Coords=input(f"{Message}")
                    if (Piece_Coords.upper()=="QUIT" or Piece_Coords.upper()=="MATE"
                        or Piece_Coords.upper()=="CHECKMATE" or Piece_Coords.upper()=="RESIGN"):
                        if self.Turn=="White":
                            Winner="Black"
                        else:
                            Winner="White"
                        from numpy import flipud
                        raise Exception(f"\nGame over, Winner = {Winner}\n{flipud(self.Board.T)}")
                    
                    try:
                        #Extract coords from string
                        Piece_Coords=Piece_Coords.split(' ')
                        if len(Piece_Coords)!=2:
                            print("Incorrect format, Try Again \U0001F622")
                            continue
                        
                        for i,Piece_Coord in enumerate(Piece_Coords):
                            Piece_Coord=int(Piece_Coord)-1
                            Piece_Coords[i]=Piece_Coord
                        #Check if a piece has been selected
                        Piece=self.Board[Piece_Coords[0]][Piece_Coords[1]]
                        if Piece != self.Empty:
                            Got_Piece_Coords=True
                            print(f"Piece Selected: {Piece}")
                        else:
                            print("Empty square selected, Try Again \U0001F622")
                    except ValueError:
                        print("Incorrect format, Try Again \U0001F622")
                    except IndexError:
                        print("Coordinates out of bounds, Try Again \U0001F622")
                
                Got_Target_Coords=False
                while Got_Target_Coords==False:
                    Failsafe+=1
                    if Failsafe>30:
                        raise RuntimeError("Too many illegal moves, consider resigning")
                    Message=f"Input Target coordinates, Turn={self.Turn}\n(Format: X Y)\n: "
                    Target_Coords=input(f"{Message}")
                    try:
                        Target_Coords=Target_Coords.split(' ')
                        for i,Target_Coord in enumerate(Target_Coords):
                            Target_Coords[i]=int(Target_Coord)-1
                        Got_Target_Coords=True
                        
                    except:
                        print("Try Again :(")
                End_of_Move=True
            return Piece,Piece_Coords,Target_Coords
                
        
        def Check_Move(self,Piece,Piece_Coords,Target_Coords):
            PX=Piece_Coords[0]
            PY=Piece_Coords[1]
            TX=Target_Coords[0]
            TY=Target_Coords[1]
            
            
            #Check whose turn
            if Piece.upper()==Piece and self.Turn!="White":
                return False
            elif Piece.upper()!=Piece and self.Turn!="Black":
                return False
            
            #Check if Target is on the board
            if TX<0 or TY<0:
                Target_Piece=self.Empty
            else:
                try: 
                    Target_Piece=self.Board[TX][TY]
                except IndexError:
                    #If target piece is off the board, assign as empty
                    Target_Piece=self.Empty
                
            #Check if target square is empty or a piece
            if Target_Piece != self.Empty and Target_Piece != None:
                #Target is a piece
                #Check target piece is of opposite colour
                if ((self.Turn!="White" and Target_Piece.islower()) 
                    or (self.Turn!="Black" and Target_Piece.isupper())):
                    #Piece is trying to capture its ally
                    return False
            
            #CHECK PAWN
            if Piece.upper()=='P':
                from Check_Pawn import Check_Pawn
                return Check_Pawn(self,Target_Piece,PX,PY,TX,TY,self.Move_List)
            #CHECK ROOK
            elif Piece.upper()=='R':
                from Check_Rook import Check_Rook
                return Check_Rook(self,PX,PY,TX,TY)
            #CHECK BISHOP
            elif Piece.upper()=='B':
                from Check_Bishop import Check_Bishop
                return Check_Bishop(self,PX,PY,TX,TY)
            #CHECK HORSE
            elif Piece.upper()=='H':
                from Check_Horse import Check_Horse
                return Check_Horse(self,PX,PY,TX,TY)
            #CHECK QUEEN
            elif Piece.upper()=='Q':
                from Check_Queen import Check_Queen
                return Check_Queen(self,PX,PY,TX,TY)
            #CHECK KING
            elif Piece.upper()=='K':
                from Check_King import Check_King
                return Check_King(self,PX,PY,TX,TY)
        
        from Check_Bounds import Check_Bounds
        from Check_Checks import Check_Checks
        from Update_Bounds import Update_Bounds
        
        Game_on=True
        self.Turn="White"
        while Game_on == True:
            #First check if in check
            Not_in_Check=Check_Checks(self,self.Board,self.White_King_Coords,self.Black_King_Coords)
            if not Not_in_Check:
                print("You are in Check!")
            
            Piece,Piece_Coords,Target_Coords=Get_Coords(self)
            Move_Legality = Check_Move(self,Piece,Piece_Coords,Target_Coords)
            Bounds_Legality= Check_Bounds(self,Piece_Coords,Target_Coords)
            
            if Move_Legality and Bounds_Legality:
                New_Board,Attrs=Update_Bounds(self,Piece,Piece_Coords,Target_Coords)
                WKC=Attrs[0]
                BKC=Attrs[1]
                Check_Legality=Check_Checks(self,New_Board,WKC,BKC)
                if Check_Legality:
                    self.Board=New_Board
                    self.White_King_Coords=WKC
                    self.Black_King_Coords=BKC
                    New_Left_Border=Attrs[2]
                    New_Right_Border=Attrs[3]
                    New_Up_Border=Attrs[4]
                    New_Down_Border=Attrs[5]
                    self.Left_Border=New_Left_Border
                    self.Right_Border=New_Right_Border
                    self.Up_Border=New_Up_Border
                    self.Down_Border=New_Down_Border
                    
                    self.Display_Board(Coords=True)
                    self.Move_List.append([Piece,Piece_Coords,Target_Coords])
                    
                    if self.Turn =="White":
                        self.Turn="Black"
                    elif self.Turn =="Black":
                        self.Turn="White"
                else:
                    print("Illegal Move, You are in Check, Try Again \U0001F622")
            else:
                print("Illegal Move, Try Again \U0001F622")
            
                
                
            
            
        
        
            
    


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
if __name__=="__main__":
    Sizes_X=[1,4]
    Sizes_Y=[3,3]
    
    A=Chess(Sizes_X,Sizes_Y)
    A.Display_Board(Coords=True)
    A.Play()
        
        
        
        
        
