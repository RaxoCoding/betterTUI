from os import walk

def initialize():
    global state 
    state = "idle"

    global current_song
    current_song = None

    global all_songs
    all_songs = next(walk("./songs"), (None, None, []))[2]
        