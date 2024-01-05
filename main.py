import pygame
import lyricsgenius
import time
import os
import mutagen.flac
import tkinter as tk
import pyaudio
from tkinter import messagebox, filedialog

status = 1
songtitle = ""
playlist = []
filename = ""
title = ""
artist = ""

def play_music():
    global title
    global artist
    try:
        filename = playlist[0]
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
        duration = pygame.mixer.Sound(filename).get_length()
        duration_minutes = int(duration // 60)
        duration_seconds = int(duration % 60)
        flac_file = mutagen.flac.FLAC(filename)
        
        sample_rate = flac_file.info.sample_rate
        bit = flac_file.info.bits_per_sample
        bitrate = flac_file.info.bitrate

        music_info = str(f'{bit} bit - {sample_rate} Hz ({int(bitrate/1000)} kbps)')
        title = flac_file["TITLE"][0]
        artist = flac_file["ARTIST"][0]
        music_data.configure(text=music_info)
        title_label.configure(text=title)
        artist_label.configure(text=artist)
        songtitle = str(f'{artist} - {title}')
        root.title(f"{songtitle}")

        if duration_minutes < 10:
            duration_minutes = "0" + str(duration_minutes)
        if duration_seconds < 10:
            duration_seconds = "0" + str(duration_seconds)
        duration_label = str(duration_minutes) + ":" + str(duration_seconds)
        while True:
            current_position = pygame.mixer.music.get_pos() / 1000
            current_minutes = int(current_position // 60)
            current_seconds = int(current_position % 60)
            if current_minutes < 10:
                 current_minutes = "0" + str(current_minutes)
            if current_seconds < 10:
                current_seconds = "0" + str(current_seconds)
            curr_timer = str(current_minutes) + ":" + str(current_seconds)
            if curr_timer == "0-1:59":
                curr_timer = "00:00"
                if len(playlist) > 1:
                    playlist.pop(0)
                    play_music()
                else:
                    pass

            timer_label.configure(text=f'{curr_timer} | {duration_label}')
            root.update()
    except:
        pass

def button_stat():
    global status
    status += 1
    if status % 2 == 0:
        pygame.mixer.music.pause()
    elif status % 2 == 1:
        status = 1
        pygame.mixer.music.unpause()

def browse_file():
    global file
    global playlist
    file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("FLAC files","*.flac"),("MP3 files","*.mp3")))
    
    playlist.append(file)

    try:
        if len(playlist) == 1:
            play_music()

    except:
        pass

def queue():
    queuelist = ""
    second_window = tk.Tk()
    second_window.geometry("240x140")
    second_window.resizable(False,False)
    second_window.title("Song Queue")
    second_window.wm_attributes("-topmost", 1)
    if len(playlist) > 0:
        lensong = 1
        for songs in playlist:
            if songs == '':
                pass
            else:
                flac_file1 = mutagen.flac.FLAC(songs)
                title1 = flac_file1["TITLE"][0]
                artist1 = flac_file1["ARTIST"][0]
                queuelist += str(f"{lensong}. {artist1} - {title1}") + "\n" 
                lensong += 1

    quelist = tk.Text(second_window)
    quelist.insert("1.0",queuelist)
    quelist.config(state="disable")
    quelist.pack()

def lyrics():
    lw = tk.Tk()
    lw.resizable(False,False)
    lw.geometry("300x200")
    lw.title("Lyrics")
    genius = lyricsgenius.Genius("") #Dear HR Team, API Hidden due security Issue
    song_name = title 
    artist_name = artist

    try:
        song = genius.search_song(song_name, artist_name)
        lyr = tk.Text(lw)
        lyr.insert("1.0",song.lyrics)
        lyr.config(state="disable")
        lyr.pack()
    except:
        pass


def next():
    if len(playlist) > 1:
        playlist.pop(0)
        play_music()

root = tk.Tk()
root.title("FLAChick 1.0.0")
root.resizable(False,False)
root.geometry("240x140")
root.configure(bg="black")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.wm_attributes("-topmost", 1)

p = pyaudio.PyAudio()
info = p.get_default_output_device_info()
default_output_device_name = info['name']

play_button = tk.Button(root, text="▶️", command=button_stat)
pause_button = tk.Button(root, text="🔁", command=play_music)
next_button = tk.Button(root, text="⏭", command=next)
browse_button = tk.Button(root, text="Browse FLAC", command=browse_file)
lyr_button = tk.Button(root,text="Lyrics",command=lyrics)
music_data = tk.Label(root, text="NA", bg="black", fg="white")
timer_label = tk.Label(root, text="00:00 | 00:00", bg="black", fg="white")
title_label = tk.Label(root, text="NA", bg="black", fg="white")
artist_label = tk.Label(root, text="NA", bg="black", fg="white")
open_button = tk.Button(root, text="Queue", command=queue)
outdev = tk.Label(root, text=str(f'Out : {default_output_device_name})'), bg="black", fg="white")

title_label.place(x =5,y=1)
artist_label.place(x =5,y=18)
timer_label.place(x =5,y=34)
music_data.place(x =5,y=50)
outdev.place(x=5,y=66)
play_button.place(x =103,y=88)
pause_button.place(x =79,y=88)
next_button.place(x =141,y=88)
browse_button.grid(row=6,column=0,sticky="nsew")
open_button.grid(row=6,column=1,sticky="nsew")
lyr_button.grid(row=6,column=2,sticky="nsew")
root.mainloop()