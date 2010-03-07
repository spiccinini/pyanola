import os
import time
import sys
from model import Partitura, Note
from parser import SSVParse

from mingus.containers import *
from mingus.midi import MidiFileIn


class TextView(object):
    def __init__(self, partitura):
        self.partitura = partitura
        self.tick = 100
        self.width = 50
        self.height = 61
        self.time = -self.tick * self.width
        a = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6]
        self.h2l = []
        for i in range(100):
            octava = i / 12
            self.h2l.append(57 - octava*7 - a[i % 12])


    def print_next(self):
        notes = []
        lines = [""] * self.height
        for instant in range(self.time, self.time + self.width * self.tick, self.tick):
            notes.append(self.partitura.sounding_at(instant))
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

        self.time += self.tick

        for line in lines:
            print line

#example = Partitura([Nota(0, 3, 300), Nota(0, 5, 300), Nota(400, 8, 300), Nota(800, 13, 600)])
from mingus.midi import fluidsynth
from mingus.containers import NoteContainer

class FluidSynthSequencer(object):
    def __init__(self, score):
        self.score = score
        self.time = 0
        self.tick = 100
    def play_next(self):
        notes = self.score._starts_at(self.time)
        container = NoteContainer([note.fluidsynthname() for note in notes])
        fluidsynth.play_NoteContainer(container)
        self.time += self.tick

def main():
    #composition = MidiFileIn.MIDI_to_Composition('test.mid')
    #score = Partitura.from_track(composition[0].tracks[4])
    score = SSVParse('libertango_piano.txt')
    view = TextView(score)
    sequencer = FluidSynthSequencer(score)
    clear = os.popen("clear").read()
    g = open('times.txt', 'w')
    start_time = time.time()
    fluidsynth.init('soundfont.sf2', 'oss')

    for i in range(max(score.notes.keys()) / view.tick):
        start_time += .1
        sys.stdout.write(clear)
        view.print_next()
        sequencer.play_next()
        now = time.time()
        if start_time > now:
            time.sleep(start_time - now)

        

if __name__ == '__main__':
    main()
