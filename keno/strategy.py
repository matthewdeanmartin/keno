# coding=utf-8
"""
Choices gambler makes in a classic gambler's ruin problem
"""

class Strategy(object):
    """
    Represents the player's risk tollerances.
    (Not the simulated player's risk tollerances!)
    """

    def __init__(self, state_range, min_ticket_price, max_ticket_price,
                 max_plays_with_ticket_type,
                 max_loss, sufficient_winnings):
        """
        Initialize self
        :type max_ticket_price: int
        :type max_plays_with_ticket_type: int
        :type max_loss: int
        :type sufficient_winnings: int
        """
        if max_loss < max_ticket_price:
            raise TypeError("Max loss > max ticket price, you know tickets often end in 0 winnings?")

        self.state_range = state_range
        self.minimum_ticket_price = min_ticket_price

        # has a relationship to max_loss
        # games also put limits on price of single ticket
        self.max_ticket_price = max_ticket_price

        # If a ticket takes 100 years to pay off, then who cares?
        self.max_plays_with_ticket_type = max_plays_with_ticket_type

        # How much is a player willing to lose (i.e. when is gambler's ruin?)
        self.max_loss = max_loss

        # How much do you want to win (i.e. a ticket that regularly wins $2 isn't exciting)
        self.sufficient_winnings = sufficient_winnings

        self.scaled_max_bet = 0.0
        # percent of net_winnings (bet more if winning more, bet less if losing/winning les)


