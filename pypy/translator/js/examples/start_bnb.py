#!/usr/bin/env python
""" bub-n-bros testing utility
"""

import autopath

import py

from pypy.translator.js import conftest

conftest.option.tg = True
conftest.option.browser = "default"

from pypy.translator.js.test.runtest import compile_function
from pypy.translator.js.modules.dom import document
from pypy.translator.js.modules.xmlhttp import XMLHttpRequest
from pypy.translator.js.modules.mochikit import log, logWarning, createLoggingPane, logDebug
from pypy.translator.js.modules.bltns import date
from pypy.translator.js.demo.jsdemo.bnb import BnbRootInstance

import time
import os

os.chdir("../demo/jsdemo")

def logKey(msg):
    #log(msg)
    pass

class Stats(object):
    """ Class containing some statistics
    """
    def __init__(self):
        self.n_received_inline_frames = 0
        self.n_rendered_inline_frames = 0
        self.n_rendered_dynamic_sprites = 0
        self.fps = 0
        self.starttime = 0.0
        self.n_sprites = 0
    
    def register_frame(self):
        self.n_rendered_inline_frames += 1
        if self.n_rendered_inline_frames >= 10:
            next_time = date()
            self.fps = 10000/(next_time - self.starttime)
            self.n_rendered_inline_frames = 0
            self.starttime = next_time

stats = Stats()

class Player(object):
    def __init__(self):
        self.id = -1
        self.prev_count = 0

player = Player()

class SpriteManager(object):
    def __init__(self):
        self.sprites = {}
        self.filenames = {}
        self.all_sprites = {}
        self.frames = []

    def add_icon(self, icon_code, filename):
        self.filenames[icon_code] = filename
        #self.sprite_queues[icon_code] = []
        #self.used[icon_code] = []
        # FIXME: Need to write down DictIterator once...
        #self.icon_codes.append(icon_code)

    def add_sprite(self, s, icon_code, x, y):
        #try:
        #    img = self.sprite_queues[icon_code].pop()
        #except IndexError:
        stats.n_sprites += 1
        img = document.createElement("img")
        img.setAttribute("src", self.filenames[icon_code])
        img.setAttribute("style", 'position:absolute; left:'+x+'px; top:'+y+'px; visibility:visible')
        document.getElementById("playfield").appendChild(img)
        try:
            self.sprites[s].style.visibility = "hidden"
            # FIXME: We should delete it
        except KeyError:
            self.sprites[s] = img
        return img

    def move_sprite(self, s, x, y):
        i = self.sprites[s]
        i.style.top = y + 'px'
        i.style.left = x + 'px'
        i.style.visibility = 'visible'

    def hide_sprite(self, s):
        i = self.sprites[s]
        i.style.visibility = "hidden"
        #pass
    
    def start_clean_sprites(self):
        self.all_sprites = {}
    
    def show_sprite(self, s, icon_code, x, y):
        self.all_sprites[s] = 1
        try:
            self.move_sprite(s, x, y)
        except KeyError:
            self.add_sprite(s, icon_code, x, y)
    
    def end_clean_sprites(self):
        for i in self.sprites:
            try:
                self.all_sprites[i]
            except KeyError:
                self.hide_sprite(i)
    
    def set_z_index(self, s_num, z):
        self.sprites[s_num].style.zIndex = z
    
    #def show_sprite(self, s):
    #    i = self.sprites[s]
    #    i.style.visibility = "visible"

sm = SpriteManager()

class KeyManager(object):
    def __init__(self):
        self.keymappings = {ord('D'):'right', ord('S'):'fire', ord('A'):'left', ord('W'):'up'}
        self.key_to_bnb_down = {'right':0, 'left':1, 'fire':3, 'up':2}
        self.key_to_bnb_up = {'right':4, 'left':5, 'fire':7, 'up':6}
        self.queue = []
            
    def add_key_up(self, key):
        self.queue.append(self.key_to_bnb_up[key])
    
    def add_key_down(self, key):
        self.queue.append(self.key_to_bnb_down[key])

    def get_keys(self):
        retval = self.queue
        self.queue = []
        return retval
    
km = KeyManager()

def appendPlayfield(msg):
    bgcolor = '#000000'
    document.body.setAttribute('bgcolor', bgcolor)
    div = document.createElement("div")
    div.setAttribute("id", "playfield")
    div.setAttribute('width', msg['width'])
    div.setAttribute('height', msg['height'])
    div.setAttribute('style', 'position:absolute; top:0px; left:0px')
    document.body.appendChild(div)

def appendPlayfieldXXX():
    bgcolor = '#000000'
    document.body.setAttribute('bgcolor', bgcolor)
    div = document.createElement("div")
    div.setAttribute("id", "playfield")
    div.setAttribute('width', 500)
    div.setAttribute('height', 250)
    div.setAttribute('style', 'position:absolute; top:0px; left:0px')
    document.body.appendChild(div)

def process_message(msg):
    if msg['type'] == 'def_playfield':
        appendPlayfield(msg)
    elif msg['type'] == 'def_icon':
        sm.add_icon(msg['icon_code'], msg['filename'])
    elif msg['type'] == 'ns':
        sm.add_sprite(msg['s'], msg['icon_code'], msg['x'], msg['y'])
        sm.set_z_index(msg['s'], msg['z'])
    elif msg['type'] == 'sm':
        sm.move_sprite(msg['s'], msg['x'], msg['y'])
        sm.set_z_index(msg['s'], msg['z'])
    elif msg['type'] == 'ds':
        sm.hide_sprite(msg['s'])
    elif msg['type'] == 'begin_clean_sprites':
        sm.start_clean_sprites()
    elif msg['type'] == 'clean_sprites':
        sm.end_clean_sprites()
    elif msg['type'] == 'show_sprite':
        sm.show_sprite(msg['s'], msg['icon_code'], msg['x'], msg['y'])
    elif msg['type'] == 'zindex':
        sm.set_z_index(msg['s'], msg['z'])
    #elif msg['type'] == 'ss':
    #    sm.show_sprite(msg['s'])
    elif msg['type'] == 'player_icon' or msg['type'] == 'def_key' or \
         msg['type'] == 'player_join' or msg['type'] == 'player_kill':
        pass #ignore
    else:
        logWarning('unknown message type: ' + msg['type'])


def addPlayer(player_id):
    name  = "player no. " + str(player_id)
    #name  = "player no. %d" % player_id
    #File "/Users/eric/projects/pypy-dist/pypy/translator/js/jts.py", line 52, in lltype_to_cts
    #    raise NotImplementedError("Type %r" % (t,))
    #    NotImplementedError: Type <StringBuilder>
    prev_player_id = player.id
    if player.id >= 0:
        #log("removing " + name)
        BnbRootInstance.remove_player(player.id, ignore_dispatcher)
        player.id = -1
    if player_id != prev_player_id:
        #log("adding " + name)
        BnbRootInstance.add_player(player_id, ignore_dispatcher)
        BnbRootInstance.player_name(player_id, name, ignore_dispatcher)
        player.id = player_id


def keydown(key):
    #c = chr(int(key.keyCode)).lower()
    #c = int(key.keyCode)
    try:
        c = key.keyCode
        if c > ord('0') and c < ord('9'):
            addPlayer(int(chr(c)))
        #for i in km.keymappings:
        #    log(str(i))
        if c in km.keymappings:
            km.add_key_down(km.keymappings[c])
        #else:
    except Exception, e:
        log(str(e))

def keyup(key):
    c = key.keyCode
    if c > ord('0') and c < ord('9'):
        pass    #don't print warning
    elif c in km.keymappings:
        km.add_key_up(km.keymappings[c])
    else:
        logWarning('unknown keyup: ' + str(c))
    
def ignore_dispatcher(msgs):
    pass

def bnb_dispatcher(msgs):
    #a = [str(i) for i in q]
    #logDebug(str(a))
    BnbRootInstance.get_message(player.id, ":".join([str(i) for i in km.get_keys()]), bnb_dispatcher)
    #sm_restart = int(msgs['add_data'][0]['sm_restart'])
    #if sm_restart == 123:
    #    log("sm_restart")
    #    stats.__init__()
    #    sm.__init__()
    #    sm.begin_clean_sprites()
    #    playfield = document.getElementById("playfield")
    #    document.body.removeChild(playfield)
    #    appendPlayfieldXXX()

##    count = int(msgs['add_data'][0]['n'])
##    if count != player.prev_count + 1:
##        logWarning("incorrect response order, expected " + str(player.prev_count+1) + ' got ' + str(count))
##        sm.frames.append(msgs)
##    player.prev_count = count
##        #else:
    #    player.prev_count = count
    #    for i in sm.frames:
    #        render_frame(i)
    render_frame(msgs)

def render_frame(msgs):
    for msg in msgs['messages']:
        process_message(msg)
    stats.register_frame()
    document.title = str(stats.n_sprites) + " sprites " + str(stats.fps)

def session_dispatcher(msgs):
    BnbRootInstance.get_message(player.id, "", bnb_dispatcher)

def run_bnb():
    def bnb():
        genjsinfo = document.getElementById("genjsinfo")
        document.body.removeChild(genjsinfo)
        createLoggingPane(True)
        log("keys: [0-9] to select player, [wsad] to walk around")
        BnbRootInstance.initialize_session(session_dispatcher)
        document.onkeydown = keydown
        document.onkeyup   = keyup
    
    from pypy.translator.js.demo.jsdemo.bnb import BnbRoot
    fn = compile_function(bnb, [], root = BnbRoot, run_browser = False)
    fn()

if __name__ == '__main__':
    run_bnb()
