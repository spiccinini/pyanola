#from mingus.containers import *
import pyglet
import cocos

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
    is_event_handler = True     #: enable pyglet's events
    def __init__(self, score):
        super(CocosNoteView, self).__init__()
        self.text = cocos.text.Label("", x=100, y=280 )

        self.score = score
        self.tick = 100
        self.time =  0
        self._accum = 0

        self.notes = []
        self.add(self.text)



    def step(self, ticks):
        self._accum -= ticks
        if self._accum <= 0:
            self._accum += self.tick
            self.time += self.tick
            self.draw()

    def step(self, ticks):
        self._accum -= ticks
        if self._accum <= 0:
            self.notes = self.score.starts_at(self.time)
                    ###############
            import pdb; pdb.set_trace()
            ###############
#            for note in notes:
#                self.add_reference_note(note)
#            result = self.validate()
#            puntos = sum([i.puntos for i in result])
            self.time += self.tick
            self._accum += self.tick


    def draw(self):

                
            
        #notes.reverse()
        print self.notes
        print self.time
"""
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
"""
