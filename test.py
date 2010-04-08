from midi_input import MidiInput, NoneInput, MidiEvent
import midi_input
from model import Score, Note
from parser import SSVParse
from sequencer import FluidSynthSequencer, MidiPlayer
from validator import Validator
from view import TextView, CocosNoteView, CocosKeyDisplay, CocosKeyboardInput
from Queue import Queue

from mingus.midi import MidiFileIn, fluidsynth
import pyglet
import cocos
from cocos.director import director

import sys
import os
import argparse
import time


def update(dt):
    try:
        dt_ticks = dt * 1000
        #sys.stdout.write(clear)
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
    #except Exception, e:
    #    print e

if __name__ == '__main__':
    director.init(resizable=True)

    #composition = MidiFileIn.MIDI_to_Composition('test.mid')
    #score = Score.from_track(composition[0].tracks[4], bpm=120)
    score = SSVParse('libertango_piano_slow.txt', 100)
    score.shift_all_notes(1000)
    view = CocosNoteView(score) #view = TextView(score)
    sequencer = FluidSynthSequencer(score)
    validator = Validator(score, margin=200)
    midi_player = MidiPlayer(validator)
    try:
        keyboard = MidiInput('/dev/midi1')
    except IOError,e:
        print e
        print "Falling back to NoneInput"
        keyboard = NoneInput()

    fluidsynth.init('soundfont.sf2', 'oss')

    step = 1/100.0
    puntos = 0

    pyglet.clock.schedule_interval(update, step)

    keyboard = CocosKeyboardInput()

    director.run( cocos.scene.Scene(CocosKeyDisplay(), keyboard, view))
