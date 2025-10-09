#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 13:32:16 2025

@author: huwtebbutt
"""

def Check_Horse(self,PX,PY,TX,TY):
    #Check L shape movement
    if (abs(TX-PX)==1 and abs(TY-PY)==2) or (abs(TX-PX)==2 and abs(TY-PY)==1):
        return True
    else: 
        return False