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

class MidiPlayer(object):
    def play(self, events):
        notes_on = (e.to_ming_note() for e in events if e.command_type ==
                'NOTE_ON')
        notes_off = (e.to_ming_note() for e in events if e.command_type ==
                'NOTE_OFF')
        fluidsynth.stop_NoteContainer(NoteContainer(notes_off))
        fluidsynth.play_NoteContainer(NoteContainer(notes_on))

