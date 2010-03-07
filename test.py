class Nota(object):
    names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'G', 'G#', 'A', 'A#', 'B']
    def name(self):
        octava = self.height / 12
        nota = self.height % 12
        print "%s%s" % (octava, names[nota])
    def __init__(self, delay, height, duration):
        self.delay = delay
        self.height = height
        self.duration = duration


class Partitura(object):
    def sounding_at(self, delay):
        return [n for n in self.notes
    def __init__(self, notas):
        self.notes = notes


class TextView(object):
    def __init__(self, partitura):
        self.time = 0
        self.partitura = partitura

    def print_next(self):
        sonando = [n for n in self.notas if

example = Partitura([Nota(0, 3, 300), Nota(400, 8, 300), Nota(800, 13, 600)])

def main():
    

if __name__ == '__main__':
    main()