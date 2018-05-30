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
    assert ticket.price() > 0

def test_ticket_validator_is_good_ticket():
    """
    Basic call
    """
    ticket = Ticket()
    tv = TicketValidator()
    assert tv.is_good_ticket(ticket)

def test_ticket_validator_basically_ok():
    """
    Basic call
    """
    ticket = Ticket()
    tv = TicketValidator()
    tv.check_ticket(ticket)
    assert True, "that function throws or doesn't no return"


def test_ticket_validator_winable():
    """
    Basic call
    """
    ticket = Ticket()
    tv = TicketValidator()
    tv.check_all_prizes_winnable(ticket)
    assert True, "that function throws or doesn't no return"
