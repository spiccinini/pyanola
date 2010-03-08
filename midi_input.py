import sys
import time
import select
import os
import mingus.core.notes as notes
import mingus.containers.Note as Note

NOTE_OFF = 0x80
NOTE_ON = 0x90
PROGRAM_CHANGE = 0xc0
ACTIVE_SENSING = 0xfe
CONTROLLER = 0xb0
PITCH_BEND = 0xe0

class MidiEvent(object):
    def __init__(self, command, data1=None, data2=None):
        self.command = command
        self.data1 = data1
        self.data2 = data2
        self.command_type = "UNKNOWN"
        if self.command == NOTE_OFF:
            self.command_type = "NOTE_OFF"
        elif self.command == NOTE_ON:
            self.command_type = "NOTE_ON"
            
    def out(self):
        result = chr(self.command) + chr(self.data1) + chr(self.data2)
        return result

    def status(self):
        return self.command & 0xf0

    def to_ming_note(self):
        note = None
        if self.command in (NOTE_OFF, NOTE_ON):
            note = Note(notes.int_to_note(self.data1 % 12), self.data1 / 12 -1)
            note.velocity = self.data2
        return note

    def __str__(self):
        return "%s %X %X %X" % (self.command_type, self.command, self.data1, self.data2)

class MidiInput(object):
    def __init__(self, filename):
        self.p = select.poll()
        self.stream = open(filename,"r")
        self.p.register(self.stream.fileno(), select.POLLIN)

    def getevent(self):
        command = ord(self.stream.read(1))
        while command == ACTIVE_SENSING:
            command = ord(self.stream.read(1))
        if command & 0xf0 in [NOTE_OFF, NOTE_ON, CONTROLLER, PITCH_BEND]:
            data1, data2 = self.stream.read(2)
            return MidiEvent(command, ord(data1), ord(data2))
        else:
            raise ValueError("Unknown event type: %s" % command)

    def poll(self):
        read = self.p.poll(0.1)
        if len(read) > 0:
            event = self.getevent()
            return event

if __name__ == "__main__":
    import time
    mi = MidiInput("/dev/midi1")
    while 1:
        event = mi.poll()
        if event:
            print event.to_ming_note(), event.command_type
