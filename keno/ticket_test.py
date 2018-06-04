# coding=utf-8
"""
Exercise ticket (a data structure) and TicketValidator, which checks ticket related game rules.
"""

from keno.ticket import Ticket, TicketValidator


def test_ticket():
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    assert ticket.price() > 0

def test_ticket_str():
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    assert "" != str(ticket)

def test_ticket_validator_is_good_ticket():
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    validator = TicketValidator()
    assert validator.is_good_ticket(ticket)

def test_ticket_validator_mutate():
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    ticket.pick()
    ticket.mutate_ticket(.5)

def test_ticket_validator_merge():
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    ticket.pick()
    second = Ticket()
    second.randomize_ticket()
    second.pick()
    ticket.geneticly_merge_ticket(second, 100)


def test_ticket_validator_basically_ok():
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    validator = TicketValidator()
    validator.check_ticket(ticket)
    assert True, "that function throws or doesn't no return"


def test_ticket_validator_winable():
    """
    Basic call
    """
    ticket = Ticket()
    validator = TicketValidator()
    validator.check_all_prizes_winnable(ticket)
    assert True, "that function throws or doesn't no return"
