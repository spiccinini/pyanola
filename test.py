from midi_input import MidiInput, NoneInput
from model import Score
from parser import SSVParse
from sequencer import FluidSynthSequencer, MidiPlayer, DummySequencer
from validator import Validator
from view import TextView, CocosNoteView, CocosKeyDisplay, CocosKeyboardInput

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

# Opciones
# * view
# * user_input
#  -> midi -> file
#  -> keyboard
# * reference_input
#  -> SSV -> file
#  -> midi_file -> file, track
# * bpm
# * audio_backend
# * soundfont file

USER_INPUTS = {"keyboard":NoneInput, "midi":MidiInput, "none":NoneInput}
VIEWS = {"text":TextView, "cocos":CocosNoteView}
INPUT_FILE_TYPES = ["midi", "ssv", "none"]
AUDIO_BACKENDS = ["oss", "alsa", "none"]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="pyanola", description='The music learning machine',
                        epilog='''
                        Usage examples:
                        python %(prog)s -r ssv -f libertango_piano_slow.txt -v cocos
                        python %(prog)s -r midi -f file.mid -t 4 -b 120 -a alsa -v text
                        ''')
    parser.add_argument('-i', '--input', action='store', choices=USER_INPUTS,
                        default="keyboard", help='select user input (default: %(default)s)')
    parser.add_argument('-m', '--midi', help='midi input. Required if -i midi(like: /dev/midi)')
    parser.add_argument('-r', '--reftype', choices=INPUT_FILE_TYPES,
                        default="none", help='reference input type (default: %(default)s)')
    parser.add_argument('-f', '--file', help='reference input file')
    parser.add_argument('-t', '--track', type=int, default=0, help='selects midi track\
                        (default: %(default)s)')
    parser.add_argument('-b', '--bpmtrack', type=int, default=120, help='selects bpm.\
                        Not implemented!.(default: %(default)s)')
    parser.add_argument('-a', '--audio', choices=AUDIO_BACKENDS, default="oss",
                        help='audio backend (default: %(default)s)')
    parser.add_argument('-s', '--soundfont', default="soundfont.sf2",
                        help='soundfont2 file (default: %(default)s)')
    parser.add_argument('-v', '--view', action='store', choices=VIEWS,
                        default="cocos", help='select view (default: %(default)s)')

    args = parser.parse_args()

    # user_input
    if args.midi:
        user_input = USER_INPUTS[args.input](args.midi)
    else:
        user_input = USER_INPUTS[args.input]()
    # reference input
    if args.reftype == "none":
        score = Score([])
    elif args.reftype == "midi":
        composition = MidiFileIn.MIDI_to_Composition(args.file)
        score = Score.from_track(composition[0].tracks[args.track], bpm=args.bpm)
    elif args.reftype == "ssv":
        score = SSVParse(args.file, 50)

    score.shift_all_notes(1000)

    # audio
    if args.audio == "none":
        sequencer = DummySequencer(score)
    elif args.audio:
        sequencer = FluidSynthSequencer(score)
        fluidsynth.init(args.soundfont, args.audio)

    #
    validator = Validator(score, margin=200)
    midi_player = MidiPlayer(validator)

    step = 1/100.0
    puntos = 0

    # view
    if issubclass(VIEWS[args.view], cocos.layer.Layer): # cualquier CocosView
        director.init()
        view = VIEWS[args.view](score)
        pyglet.clock.schedule_interval(update, step)
        keyboard = CocosKeyboardInput()
        director.run( cocos.scene.Scene(CocosKeyDisplay(), keyboard, view))
    elif args.view == "text":
        view = VIEWS[args.view](score)
        clear = os.popen("clear").read()
        keyboard = NoneInput()
        dt = 0
        last_time = now = time.time()
        while True:
            sys.stdout.write(clear)
            update(dt)
            last_time = now
            now = time.time()
            dt = now - last_time
            if step > dt:
                time.sleep(step - dt)
