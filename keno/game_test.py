# coding=utf-8
"""
Exercise game code
"""
from keno.game import NumbersMachine, Keno
from keno.number_machine import StaticNumbersMachine


def test_static_number_machine():
    """
    Basic call
    """
    machine = StaticNumbersMachine(1)
    numbers = machine.draw()
    assert len(numbers) == 1

def test_number_machine_twenty():
    """
    Basic call
    """
    machine = NumbersMachine(20)
    numbers = machine.draw_no_caching()
    assert len(numbers) == 20

def test_number_machine():
    """
    Basic call
    """
    machine = NumbersMachine(1)
    numbers = machine.draw()
    assert len(numbers) == 1


def test_keno():
    """
    Basic call
    """
    keno = Keno()
    drawing = keno.state_drawing()
    assert len(drawing) == 20
