#from mingus.containers import *
import pyglet
import cocos
import midi_input
from midi_input import MidiEvent

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
                    if note.delay < (self.width - i - 2) * self.tick + self.time:
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

class CocosNoteView(cocos.layer.Layer):
    #is_event_handler = True     #: enable pyglet's events
    def __init__(self, score):
        super(CocosNoteView, self).__init__()

        self.score = score
        self.tick = 50
        self._accum = self.tick
        self.notes = []
        self.time_corrido = 1200
        self.time =  self.time_corrido

    def step(self, ticks):
        self._accum -= ticks
        if self._accum <= 0:
            self._accum += self.tick
            self.time += self.tick
            self.notes = self.score.starts_at(self.time)
            for note in self.notes:
                text = cocos.text.Label(str(note), position=(400, (note.height-34)*16))
                action = cocos.actions.MoveBy((-700, 0), 4)
                text.do(action)
                self.add(text)

    def draw(self):
        pass

class CocosKeyboardInput(cocos.layer.ColorLayer):
    is_event_handler = True     #: enable pyglet's events
    def __init__(self):
        super(CocosKeyboardInput, self).__init__(0,0,0,0)
        self.events = []

    def on_key_press (self, key, modifiers):
        self.events.append(MidiEvent(midi_input.NOTE_ON, int(key), 120))

    def on_key_release (self, key, modifiers):
        self.events.append(MidiEvent(midi_input.NOTE_OFF, int(key), 120))

    def get_events(self):
        re = self.events[:] # FEO!s
        self.events = []
        return re

class CocosKeyDisplay(cocos.layer.Layer):
    is_event_handler = True     #: enable pyglet's events
    def __init__(self):

        super(CocosKeyDisplay, self).__init__()

        self.text = cocos.text.Label("", position=(100, 280))

        # To keep track of which keys are pressed:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
        text = 'Keys: '+','.join (key_names)
        # Update self.text
        self.text.element.text = text

    def on_key_press (self, key, modifiers):
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release (self, key, modifiers):
        self.keys_pressed.remove(key)
        self.update_text()
