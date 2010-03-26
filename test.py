import os
import sys
import time

from mingus.midi import MidiFileIn, fluidsynth

from midi_input import MidiInput, NoneInput, MidiEvent
import midi_input
from model import Score, Note
from parser import SSVParse
from sequencer import FluidSynthSequencer, MidiPlayer
from validator import Validator
from view import TextView
from Queue import Queue

# This code is so you can run the samples without installing the package
import sys
import os
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#
import pyglet
import cocos
from cocos.director import director


class KeyDisplay(cocos.layer.Layer):

    is_event_handler = True     #: enable pyglet's events

    def __init__(self):

        super( KeyDisplay, self ).__init__()

        self.text = cocos.text.Label("", x=100, y=280 )
        
        # To keep track of which keys are pressed:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
        text = 'Keys: '+','.join (key_names)
        # Update self.text
        self.text.element.text = text

    def on_key_press (self, key, modifiers):
        """This function is called when a key is pressed.
        
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
           modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
            
        """
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release (self, key, modifiers):
        """This function is called when a key is released.
        
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
           modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """
        self.keys_pressed.remove(key)
        self.update_text()


class CocosKeyboardInput(cocos.layer.Layer):
    is_event_handler = True     #: enable pyglet's events
    def __init__(self):
        super(CocosKeyboardInput, self).__init__()
        self.events = []
        
    def on_key_press (self, key, modifiers):
        """This function is called when a key is pressed.
        
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
           modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
            
        """
        
        self.events.append(MidiEvent(midi_input.NOTE_ON, int(key), 120))

    def on_key_release (self, key, modifiers):
        """This function is called when a key is released.
        
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
           modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """
        ###############
        #import pdb; pdb.set_trace()
        ###############
        self.events.append(MidiEvent(midi_input.NOTE_OFF, int(key), 120))

    def get_events(self):
        re = self.events[:] # FEO!s
        self.events = []
        return re
        
def update(dt):
    try:
        dt_ticks = dt * 1000
        sys.stdout.write(clear)
        view.step(dt_ticks)
        sequencer.step(dt_ticks)
        global keyboard
        events = keyboard.get_events()
        
        if events:
            #import pdb; pdb.set_trace()
            midi_player.play(events)

        global puntos
        puntos += validator.step(dt_ticks)

    except KeyboardInterrupt:
        pass
    except Exception, e:
        print e


if __name__ == '__main__':
    #composition = MidiFileIn.MIDI_to_Composition('test.mid')
    #score = Score.from_track(composition[0].tracks[4], bpm=120)
    score = SSVParse('libertango_piano_slow.txt', 100)
    score.shift_all_notes(1000)
    view = TextView(score)
    sequencer = FluidSynthSequencer(score)
    validator = Validator(score, margin=200)
    midi_player = MidiPlayer(validator)
    try:
        keyboard = MidiInput('/dev/midi1')
    except IOError,e:
        print e
        print "Falling back to NoneInput"
        keyboard = NoneInput()
    
    
    #keyboard = MidiInput('/dev/midi1')
    clear = os.popen("clear").read()
    g = open('times.txt', 'w')
    fluidsynth.init('soundfont.sf2', 'oss')

    # get minimum resolution of components
    step = min(view.tick, sequencer.tick) / 1000.0
    
    puntos = 0

    director.init(resizable=True)

    pyglet.clock.schedule_interval(update, step)
    # Run a scene with our event displayers:
    keyboard = CocosKeyboardInput()
    director.run( cocos.scene.Scene(KeyDisplay(), keyboard))
