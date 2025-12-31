import pygame
import sys
import math
import random
import threading
sounds=[]
fps=0
def initsounds(frame):
    global fps
    fps=frame
    print("soundsys init sucsessful")
def addsound(path,name,type,autoplay,rep):
    global sounds,fps
    sound_effect = pygame.mixer.Sound(path)
    sound={
        "name": name,
        "path": path,
        "sound": sound_effect,
        "type": type,
        "play": autoplay,
        "playing": False,
        "time_remaining": sound_effect.get_length()*fps,
        "base_time": sound_effect.get_length()*fps,
        "reps": 0,
        "rep": rep
    }
    sounds.append(sound)
def update_sounds():
    global sounds
    for sound in sounds:
        # When sound finishes playing
        if sound["time_remaining"] <= 0 and sound["playing"]:
            sound["playing"] = False
            
            # ✅ If repeat enabled, reset for next play
            if sound["rep"] and sound["play"]:
                sound["time_remaining"] = sound["base_time"]  # Reset timer
                sound["playing"] = False  # Allow restart
            else:
                sound["play"] = False  # Stop completely
        
        # Start/restart playing sound
        elif sound["play"] and not sound["playing"]:
            if sound["rep"] or sound["reps"] < 1:
                sound["time_remaining"] = sound["base_time"]  # ✅ Reset here too
                sound["sound"].play()
                sound["playing"] = True
                sound["reps"] += 1
        
        # Stop sound manually
        elif not sound["play"] and sound["playing"]:
            sound['sound'].stop()
            sound["playing"] = False
        
        # Countdown
        if sound["playing"]:
            sound["time_remaining"] -= 1

        # Debug - remove after fixing
        if sound["name"] == "your_sound_name":  # Replace with actual name
            print(f"time: {sound['time_remaining']}, playing: {sound['playing']}, play: {sound['play']}")
def stop_sound(name):
    for sound in sounds:
        if sound["name"]==name:
            sound["play"]=False
def stop_type(type):
    for sound in sounds:
        if sound["type"]==type:
            sound["play"]=False