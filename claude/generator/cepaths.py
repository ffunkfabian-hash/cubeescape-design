"""Zentrale Pfade des Claude-Generators (alles unter claude/)."""
import os
E3D=os.path.dirname(os.path.abspath(__file__))          # claude/generator/
CLAUDE=os.path.dirname(E3D)                               # claude/
ROOT=os.path.dirname(CLAUDE)                              # Repository
OUT=os.path.join(CLAUDE,'output','sheets')               # Karten / Konzeptblätter (HTML)
PREV=os.path.join(CLAUDE,'output','previews')
PROMPTS=os.path.join(CLAUDE,'prompts')
for d in (os.path.join(E3D,'reg'),os.path.join(E3D,'final'),OUT,PREV,PROMPTS):os.makedirs(d,exist_ok=True)
