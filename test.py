import os
import time

class Nota(object):
    names = [' C', 'C#', ' D', 'D#', ' E', ' F', 'F#', ' G', 'G#', ' A', 'A#', ' B']
    def __init__(self, delay, height, duration):
        self.delay = delay
        self.height = height
        self.duration = duration
    def name(self):
        octava = self.height / 12
        nota = self.height % 12
        return "%s%s" % (self.names[nota], octava)

    def __eq__(self, other):
        return self.height == other.height

    def sounding_at(self, delay):
        return self.delay <= delay <= self.delay + self.duration
    def __str__(self):
        return self.name()

class Partitura(object):
    def __init__(self, notes):
        self.notes = {}
        self.sounding_cache = set()
        self.tick = 100
        for note in notes:
            if note.delay not in self.notes:
                self.notes[note.delay] = set()
            self.notes[note.delay].add(note)

    def sounding_at(self, delay): 
        result = self._starts_at(delay)
        for i in range(60):
            result.update(n for n in self._starts_at(delay-i*self.tick) if n.sounding_at(delay))
        return result

    def _starts_at(self, delay):
        return self.notes.get(delay, set())
        



class TextView(object):
    def __init__(self, partitura):
        self.partitura = partitura
        self.tick = 100
        self.width = 50
        self.height = 11
        self.time = -self.tick * self.width

    h2l = [10, 10, 9, 9, 8, 7, 7, 6, 6, 5, 5, 4, 3, 3, 2, 2, 1, 0, 0]

    def print_next(self):
        import pprint
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

example = Partitura([Nota(0, 3, 300), Nota(0, 5, 300), Nota(400, 8, 300), Nota(800, 13, 600)])

def main():
    view = TextView(example)
    os.system('clear')
    for i in range(100):
        time.sleep(.1)
        os.system('clear')
        view.print_next()
        

if __name__ == '__main__':
    main()
