class Nota(object):
    names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'G', 'G#', 'A', 'A#', 'B']
    def __init__(self, delay, height, duration):
        self.delay = delay
        self.height = height
        self.duration = duration
    def name(self):
        octava = self.height / 12
        nota = self.height % 12
        print "%s%s" % (octava, names[nota])

    def __eq__(self, other):
        return self.height == other.height

    def sounding_at(self, delay):
        return self.delay <= delay <= self.delay + self.duration
    

class Partitura(object):
    def __init__(self, notes):
        self.notes = {}
        self.sounding_cache = set()
        for note in notes:
            if note.delay not in self.notes:
                self.notes[note.delay] = set()
            self.notes[note.delay].append(note)

    def sounding_at(self, delay):
        for note in [trash for trash in xrange(len(self.sounding_cache)) if not self.sounding_cache[trash].sounding_at(delay)]:
            self.notes.pop(note)
        self.sounding_cache+=self._starts_at(delay)
        return self.sounding_cache

    def _starts_at(self, delay):
        return self.note.get(delay, set())
        



class TextView(object):
    def __init__(self, partitura):
        self.time = 0
        self.partitura = partitura

    def print_next(self):
        sonando = set(self.partitura.sounding_at())
        for n in range(24):
            if 

example = Partitura([Nota(0, 3, 300), Nota(0, 5, 300), Nota(400, 8, 300), Nota(800, 13, 600)])

def main():
    

if __name__ == '__main__':
    main()
