# coding=utf-8
"""
Exercise ticket (a data structure) and TicketValidator, which checks ticket related game rules.
"""
from keno.strategy import Strategy
from keno.ticket import Ticket, TicketValidator


def test_ticket() -> None:
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    assert ticket.price() > 0


def test_ticket_str() -> None:
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    assert str(ticket) != ""


def test_ticket_validator_is_good_ticket() -> None:
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    validator = TicketValidator()
    assert validator.is_good_ticket(ticket)


def test_ticket_validator_mutate() -> None:
    """
    Basic call
    """
    strategy = Strategy(
        state_range=["DC", "MD"],
        min_ticket_price=0,
        max_ticket_price=100,
        max_loss=160,
        sufficient_winnings=2000,
        max_plays_with_ticket_type=365,
        evade_taxes=True,
    )
    ticket = Ticket()
    ticket.randomize_ticket()
    ticket.pick()
    ticket.mutate_ticket(.5, strategy)


def test_ticket_validator_merge() -> None:
    """
    Basic call
    """
    strategy = Strategy(
        state_range=["DC", "MD"],
        min_ticket_price=0,
        max_ticket_price=100,
        max_loss=160,
        sufficient_winnings=2000,
        max_plays_with_ticket_type=365,
        evade_taxes=True,
    )
    ticket = Ticket()
    ticket.randomize_ticket()
    ticket.pick()
    second = Ticket()
    second.randomize_ticket()
    second.pick()
    ticket.geneticly_merge_ticket(second, strategy)


def test_ticket_validator_basically_ok() -> None:
    """
    Basic call
    """
    ticket = Ticket()
    ticket.randomize_ticket()
    validator = TicketValidator()
    validator.check_ticket(ticket)
    assert True, "that function throws or doesn't no return"


def test_ticket_validator_winable() -> None:
    """
    Basic call
    """
    ticket = Ticket()
    validator = TicketValidator()
    validator.check_all_prizes_winnable(ticket)
    assert True, "that function throws or doesn't no return"
