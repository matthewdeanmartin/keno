# coding=utf-8
"""
Exercise game code
"""
from keno.game import NumbersMachine, Keno


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
