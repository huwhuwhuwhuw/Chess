#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 17:41:03 2025

@author: huwtebbutt
"""

from Board import Board
from Play import Make_Move

x_Borders=[3,3]
y_Borders=[3,3]
Board=Board(x_Borders,y_Borders)

game_on=True
while game_on:
    Make_Move(Board)