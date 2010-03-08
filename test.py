import os
import sys
import time

from mingus.midi import MidiFileIn, fluidsynth

from midi_input import MidiInput
from model import Score, Note
from parser import SSVParse
from sequencer import FluidSynthSequencer, MidiPlayer
from view import TextView


def main():
    composition = MidiFileIn.MIDI_to_Composition('test.mid')
    score = Score.from_track(composition[0].tracks[4], bpm=120)
    #score = SSVParse('libertango_piano.txt')
    score.shift_all_notes(1000)
    view = TextView(score)
    sequencer = FluidSynthSequencer(score)
    midi_player = MidiPlayer()
    keyboard = MidiInput('/dev/midi1')
    clear = os.popen("clear").read()
    g = open('times.txt', 'w')
    fluidsynth.init('soundfont.sf2', 'oss')

    # get minimum resolution of components
    step = min(view.tick, sequencer.tick, score.tick) / 1000.0
    dt = 0
    last_time = now = time.time()
    #for i in range(max(score.notes.keys()) / view.tick):
    while True:
        dt_ticks = dt * 1000
        sys.stdout.write(clear)
        view.step(dt_ticks)
        sequencer.step(dt_ticks)
        events = []
        while True:
            event = keyboard.poll()
            if event is None:
                break
            events.append(event)

        midi_player.play(events)

        last_time = now
        now = time.time()
        dt = now - last_time
        if step > dt:
            time.sleep(step - dt)

if __name__ == '__main__':
    main()
