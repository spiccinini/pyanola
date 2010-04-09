# -*- coding: utf-8 -*-
from model import Note

"""
Eventos con timestamp (delay): ON, OFF, ¿y tal vez algun otro?

Referencia contra que validar. Eventos de referencia y eventos de entrada.

add_reference_event

add_gamer_event



validar()
    return list(acierto1, acierto2, ..., miss1, miss2, ...) 
"""


#DISTANCIA OK:    A__N__B  (intervalo de 7)
#NORMAL:
#
#REF:     A___________________________B                           
#                A__________________________________B                
#                          A___B                         
#                                                   
#                                                   
#                                                   
#PLY:     A___________________________B     A________________B    
#             A_________________________________B                
#                      A_______B                         
#                                                   
#                                                   
#RSL:     B   B        M_______N______B_____M___M____________N
#

class Resultado(object):
    def __init__(self, acierto, puntos=0):
        self.puntos = puntos
        self.acierto = acierto # True o False

EVENTS = ('NOTE_ON', 'NOTE_OFF')

class EventMeta(type):
    def __new__(mcs, name, bases, _dict):
        _dict.update(dict([(const, index) for (index, const) in enumerate(EVENTS)]))
        return type.__new__(mcs, name, bases, _dict)
    def __init__(self, *atrs):
        return type.__init__(self, *atrs)

class Event(object):  
    __metaclass__ = EventMeta
    def __init__(self, type, delay, data):
        self.type = type
        self.delay = delay
        self.data = data

    def __eq__(self, other):
        return self.type == other.type and self.data.height == other.data.height

    def __str__(self):
        return "%s %s %s" % (EVENTS[self.type], self.delay, self.data)

def quantize(val, res):
    return int(val) / res * res

class Validator(object):
    def __init__(self, score, margin):
        self.reference_events = []
        self.gamer_events = []
        self.score = score
        self.tick = 100
        self.time =  0
        self._accum = 0
        self.margin = margin 

    def step(self, ticks):
        puntos = 0
        self._accum -= ticks
        if self._accum <= 0:
            notes = self.score.starts_at(self.time)
            for note in notes:
                self.add_reference_note(note)
            result = self.validate()
            puntos = sum([i.puntos for i in result])
            self.time += self.tick
            self._accum += self.tick
        return puntos

    def add_reference_event(self):
        raise NotImplementedError

    def add_gamer_event(self):
        raise NotImplementedError
        
    def add_reference_note(self, note):
        # Agrega 2 eventos, NOTE_ON y NOTE_OFF
        self.reference_events.append(Event(Event.NOTE_ON, note.delay, note))
        self.reference_events.append(Event(Event.NOTE_OFF, quantize(note.delay+note.duration, self.tick), note))

    def add_gamer_note(self, note, command_type):
        # Agrega 2 eventos, NOTE_ON y NOTE_OFF
        delay = self.time
        note = Note.from_mingus_note(note, delay)
        if command_type == 'NOTE_ON':
            self.gamer_events.append(Event(Event.NOTE_ON, note.delay, note))
        elif command_type == 'NOTE_OFF':
            self.gamer_events.append(Event(Event.NOTE_OFF, note.delay, note))
        else:
            raise NotImplementedError

    def validate(self):
        results = []
        #
        #
        # TODO: Validar que no de puntos soltar bien cuando apretaste mal.
        ref_events_to_trash = []
        gamer_events_to_trash = []
        for ref_event in self.reference_events:
            # Ver si hay un evento de gamer dentro del tiempo adecuado
            quitado = False
            for gamer_event in self.gamer_events:
                if gamer_event == ref_event:
                    # Comparacion de tiempos    
                    if ref_event.delay + self.margin >= gamer_event.delay and\
                     ref_event.delay - self.margin <= gamer_event.delay:
                        results.append(Resultado(acierto=True, puntos=10))
                        ref_events_to_trash.append(ref_event)
                        quitado = True
                        gamer_events_to_trash.append(gamer_event)
                        break
                    else:
                        results.append(Resultado(acierto=False, puntos=-10))
                        ref_events_to_trash.append(ref_event)
            # Ver si se acaba de vencer o si estaba vencida
            if not quitado:
                # Vencido?
                if self.time - self.margin > ref_event.delay:                
                    ref_events_to_trash.append(ref_event)
                    quitado = True
                    results.append(Resultado(acierto=False, puntos=-10))
        for gamer_event in self.gamer_events:
             # Vencido?
                if self.time - self.margin > gamer_event.delay:
                    results.append(Resultado(acierto=False, puntos=-10))                
                    gamer_events_to_trash.append(gamer_event)

        [self.gamer_events.remove(ev) for ev in gamer_events_to_trash]
        [self.reference_events.remove(ev) for ev in ref_events_to_trash]
        return results

        
