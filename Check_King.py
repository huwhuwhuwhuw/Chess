#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 13:39:39 2025

@author: huwtebbutt
"""

def Check_King(self,PX,PY,TX,TY):
    if abs(PX-TX)>1 or abs(PY-TY)>1:
        #King is absolutely flying
        return False
    return True