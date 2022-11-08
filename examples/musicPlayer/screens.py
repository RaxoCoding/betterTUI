import betterTUI
import globals
from datetime import datetime
from mutagen.mp3 import MP3
import pygame

def custom_exit(screen, child_obj):
    exit()

def playSong(screen, child_obj):
    audio = MP3("./songs/" +child_obj.song)

    pygame.mixer.init()  # initialize mixer module

    pygame.mixer.music.load("./songs/" + child_obj.song)

    pygame.mixer.music.play()

    globals.current_song = { 'name': child_obj.song, 'duration': audio.info.length, 'start_time': datetime.now(), 'duration_left': audio.info.length }
    return home(screen, child_obj)

def getTime():
    now = datetime.now()
    return f"Current Time: {now.strftime('%H:%M:%S')}"

def getSongStatus():

    globals.current_song['duration_left'] = globals.current_song['duration'] - (datetime.now() - globals.current_song['start_time']).total_seconds()

    min, sec = ( "%02d" % round(x) for x in divmod(globals.current_song['duration_left'], 60) )

    if(int(min) <= 0 and int(sec) <= 1):
        globals.current_song = None

    progress = '━'*(10-round((globals.current_song['duration_left']/globals.current_song['duration'])*10)) + '─'*round((globals.current_song['duration_left']/globals.current_song['duration'])*10)

    print(globals.current_song['duration_left'], globals.current_song['duration'], progress)

    return f"{progress} {min}:{sec}"

def home(screen, child_obj):

    max_y, max_x = screen.getmaxyx()

    quit_button = (betterTUI.Button(screen, 2, 3, "Quit"), custom_exit)
    search_bar = (betterTUI.SearchBar(screen, int(max_x/2-15), 2, 30, "Search Song:", "Go"), custom_exit)

    elements = [[quit_button, search_bar]]

    # navbar line
    betterTUI.Line(screen, 0, 6, '─')

    # side info line
    betterTUI.Line(screen, int(max_x/4), 3, '│', 0, True)

    # box screen
    screen.box()

    # intersection chars
    betterTUI.Text(screen, int(max_x/4), 6, "┬")
    betterTUI.Text(screen, int(max_x/4), max_y-1, "┴")

    # real time updated hours:minutes:seconds
    betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len(getTime())/2), max_y-4, getTime())

    # show current song
    if(globals.current_song):
        # Song Title
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len("Currently Playing:")/2), 10, "Currently Playing:")
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len(globals.current_song["name"][:30])/2), 11, globals.current_song['name'][:30])

        min, sec = ( "%02d" % round(x) for x in divmod(globals.current_song['duration'], 60) )

        # Song timeleft
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len(getSongStatus())/2), 13, getSongStatus())
    else:
        # Song Title
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len("Currently Playing:")/2), 10, "Currently Playing:")
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len("None")/2), 11, "None")

        # Song timeleft
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len(f"{'─'*10} 00:00")/2), 13, f"{'─'*10} 00:00")

    # List all songs

    x, y = (int(max_x/4)+2, 8)

    betterTUI.Text(screen, x, y, f"{len(globals.all_songs)} available songs:")

    for song in globals.all_songs:
        y += 3

        if(y+3 >= max_y):
            break

        button = betterTUI.Button(screen, x, y, "Play")
        button.song = song
        button = (button, playSong)

        elements.append([button])

        betterTUI.Text(screen, x+button[0].width+1, y+1, song)

    return { 'elements': elements }