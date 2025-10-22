#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 15:07:22 2025

@author: huwtebbutt
"""

    

    
def Make_Move(Board):
    #Get coordinates of move
    #Get piece coords
    def get_Piece_Coords():
        XY=input("Input piece coords:\n")
        import re
        match = re.search(r'(\d+)\D+(\d+)', XY)
        if match:
            x = int(match.group(1))-1
            y = int(match.group(2))-1
            
            return x,y
        else: return None

    #Get target coords
    def get_Target_Coords():
        XY=input("Input target coords:\n")
        import re
        match = re.search(r'(\d+)\D+(\d+)', XY)
        if match:
            x = int(match.group(1))-1
            y = int(match.group(2))-1
            return x,y
        else:
            return None
    #Check piece coords represents a piece
    def check_Piece_Coords(Board,x,y):
        Piece=Board.get_Piece(x,y)
        if Piece=='Empty':
            return False
        else:
            return True
        
    #Check attempted move is legal
    def check_Move(Board,Piece_Coords,Target_Coords):
        Piece=Board.Board[Piece_Coords[0],Piece_Coords[1]]
        #Check move complies with piece movement rules
        if not Piece.is_legal_move(Board,Target_Coords[0],Target_Coords[1]):
            return False
        
        #Check move complies with board constraints
        #Other pieces are moving opposite direction to Piece
        Relative_x=Piece_Coords[0]-Target_Coords[0]
        Relative_y=Piece_Coords[1]-Target_Coords[1]
        if not Board.check_Board_Constraints(Piece,Relative_x,Relative_y):
            return False
        
        #Update board to see if King is in check
        Old_Board=Board.Board
        New_Board=Board.Update_Board(Piece,Target_Coords[0],Target_Coords[1])
        Board.Board=New_Board
        if Board.is_Player_in_Check():
            #Player is in check at the end of their turn, illegal, revert board state
            Board.Board=Old_Board
            return False
        
        return True
    
    
    
    Board.show_board()
    print(f"Turn = {Board.Turn}")
    if Board.Check:
        print('WARNING: You are in check')
    #Set up while loop to capture coords
    Completed_Move=False
    Failsafe=0
    while Completed_Move==False:
        Failsafe+=1
        if Failsafe>10:
            raise RuntimeError("Too many incorrect attempts")
        
        Piece_Coords=get_Piece_Coords()
        if Piece_Coords:
            print(f"Piece= {Board.get_Piece(Piece_Coords[0],Piece_Coords[1]).Name}")
            PX=Piece_Coords[0]
            PY=Piece_Coords[1]
            if check_Piece_Coords(Board,PX,PY):
                Target_Coords=get_Target_Coords()
                if Target_Coords:
                    is_Move_Legal=check_Move(Board,Piece_Coords,Target_Coords)
                    if is_Move_Legal:
                        Board.Switch_Turn()
                        Completed_Move=True
                    else:
                        print('Illegal Move, try again')
                else:
                    print('Incorrect Format, try again')
            else:
                print('Incorrect Square, try again')
        else:
            print('Incorrect Format, try again')
    
if __name__ == "__main__":
    from Board import Board
    x=[2,2]
    y=[2,2]
    Board=Board(x,y)
    Make_Move(Board)
    Board.show_board()
        
    
        
    
    
    