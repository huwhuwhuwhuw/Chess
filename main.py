#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 17:41:03 2025

@author: huwtebbutt
"""

from Board import Board
from Make_Move import Make_Move

Board=Board()

game_on=True
while game_on:
    Board.show_board()
    Make_Move(Board)
    if Board.Checkmate:
        game_on=False
