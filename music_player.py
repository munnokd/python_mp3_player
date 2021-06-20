# pip install pygame

import os                          #for going to path folder
import pickle                      #to load playlist
import tkinter as Music            #its can create music GUI
from tkinter import filedialog     #used for making dialog-box
from tkinter import PhotoImage     #to display images
from pygame import mixer           #to load a background music file

# This is Music Player Logic

class Player(Music.Frame):           # this is main Player class
    def __init__(self, master=None): #this is cunstroctor
        super().__init__(master)     #super method call
        self.master = master        
        self.pack()                  #this is for load tkinter
        mixer.init()                 #this is for initially music load

        if os.path.exists('songs.pickle'):            #if path exist song can be pickle
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)        #then playlist can run
        else:                                         #if path not exist so nothing can choosen
            self.playlist = []

        self.current = 0       
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()

    def create_frames(self):  # this is for create frames for all components
        self.track = Music.LabelFrame(self, text='Song Track', font=(
            "times new roman", 15, "bold"), bg="lightgray", fg="black", bd=2, relief=Music.GROOVE)
        self.track.config(width=550, height=510)
        self.track.grid(row=0, column=0, padx=10)

        self.tracklist = Music.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}', font=(
            "times new roman", 15, "bold"), bg="lightgrey", fg="black", bd=2, relief=Music.GROOVE)
        self.tracklist.config(width=190, height=800)
        self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

        self.controls = Music.LabelFrame(self, font=(
            "times new roman", 15, "bold"), bg="lightgray", fg="gray", bd=3, relief=Music.GROOVE)
        self.controls.config(width=450, height=100)
        self.controls.grid(row=2, column=0, pady=5, padx=10)

    def track_widgets(self):  # this is for set track list styling
        self.canvas = Music.Label(self.track, image=img)
        self.canvas.configure(width=400, height=240)
        self.canvas.grid(row=0, column=0)

        self.songtrack = Music.Label(self.track, font=(
            "times new roman", 16, "bold"), bg="white", fg="coral")
        self.songtrack['text'] = 'Rockon Group'
        self.songtrack.config(width=20, height=1)
        self.songtrack.grid(row=1, column=0, padx=10)

    # this class can controll all button like pevious,play,next....
    def control_widgets(self):
        self.loadSongs = Music.Button(
            self.controls, bg='red', fg='white', font=20)
        self.loadSongs['text'] = 'Load Songs'
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.grid(row=0, column=0, padx=10)

        self.prev = Music.Button(self.controls, image=prev)
        self.prev['command'] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause = Music.Button(self.controls, image=pause)
        self.pause['command'] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.next = Music.Button(self.controls, image=next_)
        self.next['command'] = self.next_song
        self.next.grid(row=0, column=3)

        self.volume = Music.DoubleVar(self)
        self.slider = Music.Scale(self.controls, from_=0,to=10, orient=Music.HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(10)
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)

    # this can give styling and set for track list designing
    def tracklist_widgets(self):
        self.scrollbar = Music.Scrollbar(self.tracklist, orient=Music.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.list = Music.Listbox(self.tracklist, selectmode=Music.SINGLE,yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
        self.enumerate_songs()
        self.list.config(height=22, width=40)
        self.list.bind('<Double-1>', self.play_song)

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    # this class can be pick songs from folder which can provided by us
    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()                #this can take music directory
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\', '/')
                    self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)           #for adding song one  by one 
        self.playlist = self.songlist
        self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
        self.list.delete(0, Music.END)
        self.enumerate_songs()

    # this can add all song to tracklist which folder can provided by us
    def enumerate_songs(self):                                   
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def play_song(self, event=None):  # this class for play song
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        print(self.playlist[self.current])
        mixer.music.load(self.playlist[self.current])
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])

        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='sky blue')

        mixer.music.play()

    def pause_song(self):  # this class for pause song
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

    def prev_song(self):  # this class for go to previous song
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.play_song()

    def next_song(self):  # this class for go to next song
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='white')
        self.play_song()

    def change_volume(self, event=None):  # this class for change volume of song
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)

# this is music player Ui


root = Music.Tk()                            # play sound in python
root.geometry('800x400')                     # this can give box a sizing when we start our app

# this all are fetch images from my folder
img = PhotoImage(file='images/Music.png')
next_ = PhotoImage(file='images/Next.png')
prev = PhotoImage(file='images/Prev.png')
play = PhotoImage(file='images/Play.png')
pause = PhotoImage(file='images/Pause.png')

app = Player(master=root)  # Call Player class and pass root in music frame 
app.mainloop()             # to run the Tkinter event loop and call GUI
