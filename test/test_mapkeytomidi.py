import unittest
import sys
sys.path.append('..')

from pyglet.window import key as K
from mapkeytomidi import MapKeyToMidi

class MapKeyToMidiTestCase(unittest.TestCase):

    def test_notes(self):
        map_key = MapKeyToMidi()
        self.assertEqual(60, map_key(K.A))
        self.assertEqual(62, map_key(K.S))
        self.assertEqual(72, map_key(K.K))
        self.assertEqual(61, map_key(K.W))
        self.assertEqual(73, map_key(K.O))

    def test_change_octave(self):
        map_key = MapKeyToMidi()
        self.assertEqual(60, map_key(K.A))
        map_key.octave = 3
        self.assertEqual(48, map_key(K.A))
        self.assertEqual(60, map_key(K.K))
    def test_change_withkeys(self):
        map_key = MapKeyToMidi()
        self.assertEqual(60, map_key(K.A))

        self.assertRaises(KeyError, map_key, K.LSHIFT)
        self.assertRaises(KeyError, map_key,K.LSHIFT)
        self.assertEqual(48, map_key(K.A))



if __name__ == '__main__':
    unittest.main()
