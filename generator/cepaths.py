"""Zentrale Pfade des Generators (relativ zum Repository)."""
import os
E3D=os.path.dirname(os.path.abspath(__file__))          # generator/
ROOT=os.path.dirname(E3D)
OUT=os.path.join(ROOT,'output','sheets')                 # fertige Karten / Konzeptblätter (HTML)
PREV=os.path.join(ROOT,'output','previews')
os.makedirs(os.path.join(E3D,'reg'),exist_ok=True);os.makedirs(os.path.join(E3D,'final'),exist_ok=True);os.makedirs(OUT,exist_ok=True)
