from bisect import bisect_left
class Note(object):
    names = [' C', 'C#', ' D', 'D#', ' E', ' F', 'F#', ' G', 'G#', ' A', 'A#', ' B']
    def __init__(self, delay, height, duration):
        self.delay = delay
        self.height = height
        self.duration = duration
        self.octave = self.height / 12
        self.note = self.height % 12

    def name(self):
        return "%s%s" % (self.names[self.note], self.octave)

    def fluidsynthname(self):
        """Name we can feed to fluidsynth"""
        return "%s-%s" % (self.names[self.note].strip(), self.octave)

    def __eq__(self, other):
        return self.height == other.height

    def sounding_at(self, delay):
        return self.delay <= delay < self.delay + self.duration

    def __repr__(self):
        return "<Note:%s %s>" % (self.name(), self.duration)

    @classmethod
    def from_mingus_note(self, note, delay):
        height = int(note)
        duration = 0
        return Note(delay, height, duration)

class NoteSet(object):
    def __init__(self, delay):
        self.delay = delay
        self.notes = set()
    def __iter__(self):
        return self.notes.__iter__()
    def add(self, note):
        self.notes.add(note)
    def __lt__(self, other):
        return self.delay < other.delay
    def update(self, notes):
        for n in notes:
            self.add(n)
    def shift(self, delay):
        self.delay += delay
    def __len__(self):
        return len(self.notes)
    def __repr__(self):
        names = [str(n) for n in self.notes]
        return "<Noteset(%s):[%s]>" % (self.delay, ','.join(names))

class Score(object):
    def __init__(self, notes):
        self._starts_at = {}
        self._ends_at = {}
        self._sounding_at = []
        for note in notes:
            self.add(note)

    def add(self, note):
        # Add to _starts_at
        if note.delay not in self._starts_at:
            self._starts_at[note.delay] = set()
        self._starts_at[note.delay].add(note)
        # Add to _ends_at
        if note.delay + note.duration not in self._ends_at:
            self._ends_at[note.delay + note.duration] = set()
        self._ends_at[note.delay + note.duration].add(note)
        # Add to sounding_at
        start = NoteSet(note.delay)
        start_idx = bisect_left(self._sounding_at, start)
        if (start_idx == len(self._sounding_at) or
            note.delay != self._sounding_at[start_idx].delay):
            if start_idx > 0:
                start.update(self._sounding_at[start_idx - 1])
            self._sounding_at.insert(start_idx, start)
        end = NoteSet(note.delay + note.duration)
        end_idx = bisect_left(self._sounding_at, end)
        if (end_idx == len(self._sounding_at) or
            note.delay + note.duration != self._sounding_at[end_idx].delay):
            if end_idx < len(self._sounding_at):
                end.update(self._sounding_at[end_idx])
            self._sounding_at.insert(end_idx, end)
        for i in xrange(start_idx, end_idx):
            self._sounding_at[i].add(note)
        
    def sounding_at(self, delay):
        noteset = NoteSet(delay)
        idx = bisect_left(self._sounding_at, noteset)
        if idx == len(self._sounding_at):
            return noteset
        elif delay == self._sounding_at[idx].delay:
            return self._sounding_at[idx]
        elif idx == 0:
            return noteset
        else:
            return self._sounding_at[idx-1]

    def starts_at(self, delay):
        return self._starts_at.get(delay, set())

    def ends_at(self, delay):
        return self._ends_at.get(delay, set())

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
        new_starts_at = {}
        for d, notes in self._starts_at.items():
            new_starts_at[delay + d] = set()
            for note in notes:
                note.delay += delay
                new_starts_at[delay + d].add(note)
        self._starts_at = new_starts_at

        new_ends_at = {}
        for d, notes in self._ends_at.items():
            new_ends_at[delay + d] = set()
            for note in notes:
                new_ends_at[delay + d].add(note)
        self._ends_at = new_ends_at

        for noteset in self._sounding_at:
            noteset.shift(delay)
