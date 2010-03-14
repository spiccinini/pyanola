import os
import sys
import time

from mingus.midi import MidiFileIn, fluidsynth

from midi_input import MidiInput, NoneInput
from model import Score, Note
from parser import SSVParse
from sequencer import FluidSynthSequencer, MidiPlayer
from validator import Validator
from view import TextView


def main():
    #composition = MidiFileIn.MIDI_to_Composition('test.mid')
    #score = Score.from_track(composition[0].tracks[4], bpm=120)
    score = SSVParse('libertango_piano.txt', 100)
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

    clear = os.popen("clear").read()
    g = open('times.txt', 'w')
    fluidsynth.init('soundfont.sf2', 'oss')

    # get minimum resolution of components
    step = min(view.tick, sequencer.tick) / 1000.0
    dt = 0
    last_time = now = time.time()
    #for i in range(max(score.notes.keys()) / view.tick):
    puntos = 0
    try:
        while True:
            dt_ticks = dt * 1000
            sys.stdout.write(clear)
            
            view.step(dt_ticks)
            sequencer.step(dt_ticks)
            
            events = keyboard.get_events()
            if events:
                midi_player.play(events)

            puntos += validator.step(dt_ticks)

            last_time = now
            now = time.time()
            dt = now - last_time
            if step > dt:
                time.sleep(step - dt)
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print e

    print 'Total de puntos: ', puntos

if __name__ == '__main__':
    main()
