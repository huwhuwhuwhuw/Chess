#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 12:27:53 2025

@author: huwtebbutt
"""

def Make_Move(Board,Piece_Coords=None,Target_Coords=None):
    # =============================================================================
    def get_Piece_Coords():
        #Searches an input for any 2 numbers
        #Returns these two numbers
        Input=input("Input piece coords:\n")
        from re import search
        match = search(r'(\d+)\D+(\d+)', Input)
        if match:
            x = int(match.group(1))-1
            y = int(match.group(2))-1
            return x,y
        else: 
            return None

    def get_Target_Coords():
        #Searches an input for any 2 numbers
        #Returns these two numbers
        Input=input("Input target coords:\n")
        from re import search
        match = search(r'(\d+)\D+(\d+)', Input)
        if match:
            x = int(match.group(1))-1
            y = int(match.group(2))-1
            return x,y
        else:
            return None
    def check_Piece_Coords(Board,x,y):
        #Check that the piece coords correspond to the right square
        #return True/False
        Piece=Board.get_Piece(x,y)
        if Piece=='Empty':
            #Piece coords must point to a piece
            print("Empty Square, try again")
            return False
        else:
            Confirmation = False
            from re import findall
            Breaker=0
            while not Confirmation:
                Confirmation= input("Correct Piece? y/n\n")
                #Clean up input, only care about letters
                Confirmation = ''.join(findall(r'[a-zA-Z]', Confirmation))
                if Confirmation:
                    #Check first letter, assume user will input some form of Yes,Yeah,Y,y,yes / No,n,N
                    if Confirmation.upper()[0]=='Y':
                        return True
                    else:
                        print("Selected wrong square")
                        return False
                Breaker+=1
                if Breaker>10:
                    raise RuntimeError
    def Attempt_Move(Board,Piece_Coords,Target_Coords):
        #Try the move, and check that it is all legal
        #Return true/false based on if move is legal
        
        Piece=Board.Board[Piece_Coords[0],Piece_Coords[1]]
        #Check move complies with piece movement rules
        if not Piece.is_legal_move(Board,Target_Coords[0],Target_Coords[1]):
            print('Illegal Move')
            return False
        
        #Check move complies with board constraints
        #Other pieces are moving opposite direction to Piece
        Relative_x=Piece_Coords[0]-Target_Coords[0]
        Relative_y=Piece_Coords[1]-Target_Coords[1]
        if not Board.check_Board_Constraints(Piece,Relative_x,Relative_y):
            print('Board constraints')
            return False
        
        #Update board and see if King is in check
        #Keep copy of board to revert to if new board is illegal
        Old_Board=Board.Board
        Board.Board=Board.Update_Board(Piece,Target_Coords[0],Target_Coords[1])
        if Board.is_Player_in_Check():
            #Player is in check at the end of their turn, illegal, revert board state
            Board.Board=Old_Board
            Piece=Board.get_Piece(Piece_Coords[0],Piece_Coords[1])
            if Piece.Castling:
                Piece.Castling=False
            elif Piece.EnPassanting:
                Piece.EnPassanting=False
            print('Check issue')
            return False
        #No exceptions found, legal move, board has been updated, return true
        return True
    # =============================================================================
    if Piece_Coords and Target_Coords:
        #Check Piece Coords points to a piece
        Piece=Board.get_Piece(Piece_Coords)
        if Piece=='Empty':
            print('Empty Piece')
            return False
        if Attempt_Move(Board,Piece_Coords,Target_Coords):
            Board.Switch_Turn()
            Board.Move_List.append([Piece,Piece_Coords,Target_Coords])
            if Board.is_Checkmate():
                Board.Checkmate=True
                for i,row in enumerate(Board.Board):
                    for j,square in enumerate(row):
                        if square.Colour==Board.Turn and square!='King':
                            Board.Board[i,j]='Empty'
            return True
        else:
            print('Attempt Failed')
            return False
    else:
        #Coords not provided, get from user
        Piece_Coords=get_Piece_Coords()
        if Piece_Coords:
            #user has inputted target coords
            Piece=Board.get_Piece(Piece_Coords[0],Piece_Coords[1])
            print(f"Piece= {Piece.Colour} {Piece.Name}")
            PX=Piece_Coords[0]
            PY=Piece_Coords[1]
            if check_Piece_Coords(Board,PX,PY):
                #Coords point to a piece and user has confirmed their choice
                Target_Coords=get_Target_Coords()
                if Target_Coords:
                    #user has inputed target coords
                    if Attempt_Move(Board,Piece_Coords,Target_Coords):
                        #Move has been sucessfully implemented
                        Board.Switch_Turn()
                        #Record move
                        Board.Move_List.append([Piece,Piece_Coords,Target_Coords])
                        #Check for Checkmate
                        if Board.is_Checkmate():
                            print("Checkmate!")
                            Board.Checkmate=True
                            #delete all losing pieces
                            for i,row in enumerate(Board.Board):
                                for j,square in enumerate(row):
                                    if square.Colour==Board.Turn and square!='King':
                                        Board.Board[i,j]='Empty'
                        else: 
                            #not checkmate
                            print("Move successfull")
                        return True
                    else:
                        #Move failed to be implemented
                        print('Illegal Move, try again')
                        return False
                        
                else:
                    #Incorrect target coords format
                    print('Incorrect Format, try again')
                    return False
            else:
                #Either user didnt confirm, or piece coords point towards empty square
                return False
        else:
            #Incorrect piece coords format
            print('Incorrect Format, try again')
            return False
                

