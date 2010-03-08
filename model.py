
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

    def fluidsynthname(self):
        """Name we can feed to fluidsynth"""
        octave = self.height / 12
        note = self.height % 12
        return "%s-%s" % (self.names[note].strip(), octave)

    def __eq__(self, other):
        return self.height == other.height

    def sounding_at(self, delay):
        return self.delay <= delay <= self.delay + self.duration

    def __repr__(self):
        return "<Note: %s %s>" % (self.name(), self.duration)

class Score(object):
    def __init__(self, notes):
        self.notes = {}
        self.sounding_cache = set()
        self.tick = 50
        for note in notes:
            note.delay = int(note.delay / 100) * 100
            if note.delay not in self.notes:
                self.notes[note.delay] = set()
            self.notes[note.delay].add(note)

    _sounding_at_cache = {}

    def sounding_at(self, delay):
        if delay in self._sounding_at_cache:
            return self._sounding_at_cache[delay]
        result = self._starts_at(delay)
        for i in range(60):
            result.update(n for n in self._starts_at(delay-i*self.tick) if n.sounding_at(delay))
        self._sounding_at_cache[delay] = result
        return result

    def _starts_at(self, delay):
        return self.notes.get(delay, set())

    @classmethod
    def from_track(cls, track, bpm=120):
        notes = []
        ticks_per_minute = 60000
        beats_per_bar = 4
        ticks_per_bar = ticks_per_minute * beats_per_bar / bpm
        for i, bar in enumerate(track):
            for note in bar:
                delay = (note[0] + i) * ticks_per_bar
                for n in note[2].notes:
                    height = int(n)
                    if note[1] != 0.0:
                        duration = (1.0 / note[1]) * ticks_per_bar
                        notes.append(Note(delay, height, duration))

        instance = Score(notes)
        return instance

    def shift_all_notes(self, delay):
        new_notes = {}
        for d in self.notes:
            new_notes[delay+d] = set()
            for note in self.notes[d]:
                note.delay += delay
                new_notes[note.delay].add(note)
        self.notes = new_notes

