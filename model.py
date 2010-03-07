
class Note(object):
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
            note.delay = int(note.delay / 100) * 100
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
        



