import os
import time
import sys
from model import Score, Note
from parser import SSVParse
from validator import Validator

from mingus.containers import *
from mingus.midi import MidiFileIn


class TextView(object):
    def __init__(self, score):
        self.score = score
        self.tick = 100
        self.width = 50
        self.height = 61
        self.time = 0
        self._accum = self.tick

        a = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6]
        self.h2l = []
        for i in range(100):
            octava = i / 12
            self.h2l.append(57 - octava*7 - a[i % 12])

    def step(self, ticks):
        self._accum -= ticks
        if self._accum <= 0:
            self._accum += self.tick
            self.time += self.tick
            self.draw()

    def draw(self):
        notes = []
        lines = [""] * self.height
        for instant in range(self.time, self.time + self.width * self.tick, self.tick):
            notes.append(self.score.sounding_at(instant))
        notes.reverse()

        i = 0
        for instant in notes:
            if i == self.width - 1:
                template = "[%s]"
            else:
                template = "%s"
            for note in instant:
                if len(lines[self.h2l[note.height]]) < 3 * i:
                    if note.delay < (self.width - i - 1) * self.tick + self.time:
                        lines[self.h2l[note.height]] +=template%"..."
                    else:
                        lines[self.h2l[note.height]]+=template%note.name()
            for line_index, line in enumerate(lines):
                stripe = ['---', '   '][line_index % 2]
                if len(line) < 3 * i:
                    lines[line_index] += template%stripe
            i += 1

        for line in lines:
            print line

from mingus.midi import fluidsynth
from mingus.containers import NoteContainer

class FluidSynthSequencer(object):
    def __init__(self, score):
        self.score = score
        self.time = 0
        self.tick = 20
        self._accum = self.tick

    def step(self, ticks):
        self._accum -= ticks
        if self._accum <= 0:
            self.play()
            self.time += self.tick
            self._accum += self.tick

    def play(self):
        notes = self.score._starts_at(self.time)
        container = NoteContainer([note.fluidsynthname() for note in notes])
        fluidsynth.play_NoteContainer(container)

def main():
    #composition = MidiFileIn.MIDI_to_Composition('test.mid')
    #score = Score.from_track(composition[0].tracks[4], bpm=90)
    score = SSVParse('libertango_piano_slow.txt', resolution = 100)
    score.shift_all_notes(2000)
    #composition = MidiFileIn.MIDI_to_Composition('test.mid')
    #score = Score.from_track(composition[0].tracks[4], bpm=120)
    #score = SSVParse('libertango_piano.txt')
    #score.shift_all_notes(1000)
    view = TextView(score)
    sequencer = FluidSynthSequencer(score)
    validator = Validator(score, margin=200)
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
        #start_time += dt
        sys.stdout.write(clear)
        validator.step(dt_ticks)
        view.step(dt_ticks)
        sequencer.step(dt_ticks)
        
        last_time = now
        now = time.time()
        dt = now - last_time
        if step > dt:
            time.sleep(step - dt)
        #now = time.time()
        #dt = now - start_time
        #if step > dt:
        #    time.sleep(step - dt)
        #start_time += dt


if __name__ == '__main__':
    main()
