import os
import time
import sys
from model import Partitura, Note
from parser import SSVParse


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

def main():
    score = SSVParse('libertango_piano.txt')
    view = TextView(score)
    clear = os.popen("clear").read()
    g = open('times.txt', 'w')
    start_time = time.time()
    for i in range(max(score.notes.keys()) / view.tick):
        start_time += .1
        sys.stdout.write(clear)
        view.print_next()
        time.sleep(start_time - time.time())

        

if __name__ == '__main__':
    main()
