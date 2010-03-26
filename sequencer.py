from mingus.midi import fluidsynth
from mingus.containers import NoteContainer

class FluidSynthSequencer(object):
    def __init__(self, score):
        self.score = score
        self.time = 0
        self.played = set()
        self.tick = 10

    def step(self, ticks):
        self.time += ticks
        new = [n for n in self.score.sounding_at(self.time) if not n in self.played]
        container = NoteContainer([note.fluidsynthname() for note in new])
        fluidsynth.play_NoteContainer(container)
        remove = [n for n in self.played if self.time >= n.delay + n.duration]
        self.played.difference_update(remove)
        self.played.update(new)

class MidiPlayer(object):
    def __init__(self, validator):
        self.validator = validator

    def play(self, events):
        notes_on = [e.to_ming_note() for e in events if e.command_type == 'NOTE_ON']
        notes_off = [e.to_ming_note() for e in events if e.command_type == 'NOTE_OFF']
        #import pdb; pdb.set_trace()
        for note in notes_off:
            self.validator.add_gamer_note(note, 'NOTE_OFF')
        fluidsynth.stop_NoteContainer(NoteContainer(notes_off))
        for note in notes_on:
            self.validator.add_gamer_note(note, 'NOTE_ON')
        fluidsynth.play_NoteContainer(NoteContainer(notes_on))

