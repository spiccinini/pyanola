from copy import copy
import unittest
import sys
sys.path.append('..')

from model import Note, Score

class TestScore(unittest.TestCase):
    def test_single_note(self):
        a = Note(100, 15, 250)
        score = Score([a])
        for i in [40, 99, 101, 349, 350, 341, 450]:
            self.assertEquals(0, len(score.starts_at(i)))
        self.assertEquals(1, len(score.starts_at(100)))

        for i in [40, 99, 100, 101, 349, 351, 450]:
            self.assertEquals(0, len(score.ends_at(i)))
        self.assertEquals(1, len(score.ends_at(350)))

        for i in [50, 99, 350, 351, 450]:
            self.assertEquals(0, len(score.sounding_at(i)))
        for i in [100, 101, 349]:
            self.assertEquals(1, len(score.sounding_at(i)))


    def test_chord(self):
        a = Note(100, 15, 250)
        b = Note(100, 11, 250)
        c = Note(100, 18, 250)
        score = Score([a, b, c])
        for i in [40, 99, 101, 349, 350, 351, 450]:
            self.assertEquals(0, len(score.starts_at(i)))
        self.assertEquals(3, len(score.starts_at(100)))

        for i in [40, 99, 100, 101, 349, 351, 450]:
            self.assertEquals(0, len(score.ends_at(i)))
        self.assertEquals(3, len(score.ends_at(350)))

        for i in [50, 99, 350, 351, 450]:
            self.assertEquals(0, len(score.sounding_at(i)))
        for i in [100, 101, 349]:
            self.assertEquals(3, len(score.sounding_at(i)))

    def test_interval(self):
        a = Note(100, 15, 200)
        b = Note(200, 11, 200)
        c = Note(300, 18, 200)
        score = Score([a, b, c])
        for i in [40, 99, 101, 199, 201, 299, 301, 400, 500]:
            self.assertEquals(0, len(score.starts_at(i)))
        for i in [100, 200, 300]:
            self.assertEquals(1, len(score.starts_at(i)))

        for i in [40, 99, 100, 101, 200, 201, 299, 301, 499]:
            self.assertEquals(0, len(score.ends_at(i)))
        for i in [300, 400, 500]:
            self.assertEquals(1, len(score.ends_at(i)))

        for i in [50, 99, 500]:
            self.assertEquals(0, len(score.sounding_at(i)))
        for i in [100, 101, 199, 400, 499]:
            self.assertEquals(1, len(score.sounding_at(i)))
        for i in [200, 201, 299, 300, 301, 399]:
            self.assertEquals(2, len(score.sounding_at(i)))

    def test_shift(self):
        a = Note(100, 15, 250)
        shift = 100
        score = Score([copy(a)])
        score.shift_all_notes(shift)
        for i in [140, 199, 201, 449, 450, 451, 550]:
            self.assertEquals(0, len(score.starts_at(i)))
        self.assertEquals(1, len(score.starts_at(200)))

        for i in [140, 199, 200, 201, 449, 451, 550]:
            self.assertEquals(0, len(score.ends_at(i)))
        self.assertEquals(1, len(score.ends_at(450)))

        for i in [150, 199, 450, 451, 550]:
            self.assertEquals(0, len(score.sounding_at(i)))
        for i in [200, 201, 449]:
            self.assertEquals(1, len(score.sounding_at(i)))

        notes = score.starts_at(200)
        for n in notes:
            self.assertEquals(n.delay, a.delay + shift)

if __name__ == '__main__':
    unittest.main()
