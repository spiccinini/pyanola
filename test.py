class Nota(object):
    names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'G', 'G#', 'A', 'A#', 'B']
    def __init__(self, delay, height, duration):
        self.delay = delay
        self.height = height
        self.duration = duration
    def name(self):
        octava = self.height / 12
        nota = self.height % 12
        print "%s%s" % (octava, names[nota])
    def __eq__(self, other):
        return self.height == other.height

    def sounding_at(self, delay):
        return self.delay <= delay <= self.delay + self.duration

class Partitura(object):
    def sounding_at(self, delay):
        return [n for n in self.notes if n.sounding_at(delay)]

    def __init__(self, notas):
        self.notes = notes


class TextView(object):
    def __init__(self, partitura):
        self.time = 0
        self.partitura = partitura

    def print_next(self):
        sonando = set(self.partitura.sounding_at())
        for n in range(24):
            if 

example = Partitura([Nota(0, 3, 300), Nota(400, 8, 300), Nota(800, 13, 600)])

def main():
    

if __name__ == '__main__':
    main()