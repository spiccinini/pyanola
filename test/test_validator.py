import unittest
import sys
sys.path.append('..')

from model import Note, Score
from validator import Validator, Event

class TestValidatorSingleNote(unittest.TestCase):
    def setUp(self):
        """
        Create a validator and add one note to it.
        Note(delay=100, height=15, duration=100)
        """
        self.the_note = Note(delay=100, height=15, duration=100)
        score = Score([self.the_note])
        self.validator = Validator(score, margin=10)
        self.validator.add_reference_note(self.the_note)

    def test_single_note_miss(self):
        """
        Checks that without user input the validator generates
        the coorect results.
        """
        for t in [99, 100, 109, 110, 111, 199, 201, 210, 211, 220]:
            self.validator.time = t
            results = self.validator.validate()
            if t  in [111, 211]:
                self.assertEquals(False, results[0].acierto)
            else:
                self.assertEquals(0, len(results))

    def test_single_note_perfect_hit(self):
        """
        Checks that with the correc user input the validator generates
        the coorect results.
        """
        note = self.the_note
        for t in [50, 80, 90, 99, 100, 109, 110, 111, 199, 200, 210, 211, 220]:
            if t == 100:
                self.validator.add_gamer_event(Event(Event.NOTE_ON, note.delay, note))
            if t == 200:
                self.validator.add_gamer_event(Event(Event.NOTE_OFF, t, note))
            self.validator.time = t
            results = self.validator.validate()
            if t  in [100, 200]:
                self.assertEquals(True, results[0].acierto)
            else:
                self.assertEquals(0, len(results))

    def test_single_note_hit_extremes(self):
        """
        Checks that with the correc user input the validator generates
        the coorect results.
        """
        note = self.the_note
        for t in [50, 80, 90, 99, 100, 109, 110, 111, 199, 200, 210, 211, 220]:
            if t == 90:
                self.validator.add_gamer_event(Event(Event.NOTE_ON, note.delay, note))
            if t == 210:
                self.validator.add_gamer_event(Event(Event.NOTE_OFF, t, note))
            self.validator.time = t
            results = self.validator.validate()
            if t  in [90, 210]:
                self.assertEquals(True, results[0].acierto)
            else:
                self.assertEquals(0, len(results))

    def test_single_note_miss_extremes(self): # BUG
        """
        Checks that with the correc user input the validator generates
        the coorect results.
        """
        note = self.the_note
        for t in [50, 89, 90, 99, 100, 101, 110, 111, 199, 200, 210, 211, 220]:
            if t == 89:
                self.validator.add_gamer_event(Event(Event.NOTE_ON, t, note))
                #import pdb;pdb.set_trace()
            if t == 211:
                self.validator.add_gamer_event(Event(Event.NOTE_OFF, t, note))
            self.validator.time = t
            results = self.validator.validate()
            #print t, [str(r) for r in results]
            #if t  in [89, 211]:
            #    self.assertEquals(True, results[0].acierto)
            #else:
            #    self.assertEquals(0, len(results))

    def test_fix_x_not_in_list(self): 
        """
        Fixed ValueError: list.remove(x): x not in list bug.
        """
        note = self.the_note
        for t in [50, 90, 99, 100, 109, 110, 111, 199, 200, 210, 211, 220]:
            if t == 211:
                self.validator.add_gamer_event(Event(Event.NOTE_OFF, t, note))
            self.validator.time = t
            results = self.validator.validate()





if __name__ == '__main__':
    unittest.main()
