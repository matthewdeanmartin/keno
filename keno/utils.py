# coding=utf-8
"""
Poorly named, this is the main code.
"""
import copy
import sys
from collections import OrderedDict

from keno.game import Keno
from keno.player import Player
from keno.ticket import Ticket


def run():
    """
    Execute main simulator
    :return:
    """
    tickets = []

    # vacuously, the more you bet, the more likley you are to win something
    max_ticket_price = 50

    # possibly inefficient way of generating all possible tickets.
    # I'm not sure how big the total space is.
    print("Generating tickets...")
    sys.stdout.flush()
    for i in range(0, 50000):
        ticket = Ticket()
        ticket.randomize_ticket()
        if ticket in tickets:
            continue
        # TODO: check minimum winning on 1 ticket!!
        # if ticket.spots>10:
        #     continue
        # if ticket.spots <4:
        #     continue
        # # if not (ticket.bonus or ticket.super_bonus):
        # #     ticket.super_bonus=True
        # #     ticket.bonus =False
        if ticket.price() > max_ticket_price:
             continue

        tickets.append(ticket)

    print("Have {0} tickets. Now ready to play".format(len(tickets)))
    sys.stdout.flush()
    winners = {
        0:tickets,
    }
    """:type: list[Ticket]"""

    md_keno = Keno()
    for generation in range(0, 20):
        print("Generation {0}".format(generation))
        # round 2+, iterate winners, not orig tickets

        current_tickets = winners[generation]
        winners[generation+1] = []

        i = 0
        print("Now playing {0} tickets ".format(len(current_tickets)))
        for ticket in current_tickets:
            i +=1
            jackpot = 2500
            if not md_keno.can_i_win_this_much(ticket, jackpot):
                # loser ticket.
                continue
            if ticket.price()> max_ticket_price:
                # costs too much now... loser
                continue

            player = Player(500, jackpot, 50)
            # override ticket
            player.ticket = ticket

            player.go()
            if player.good_game():
                winners[generation + 1].append(ticket)
                if i<6:
                    print("------Good Game------" + str(ticket.price() * player.tickets_played))
                else:
                    print('.', end='')

                # print(ticket)
                # print("Ticket Price: {0}".format(ticket.price()))
                # print(player)
                # print("-----")
                # print(md_keno.possible_pay_off_for_ticket_per_game(ticket))

        remaining = len(winners[generation+1])
        print("Remaining winners: {0}".format(remaining))
        if remaining == 0:
            print("All tickets suck")
            break

        print("Crossing Tickets")
        upcoming_generation = winners[generation+1]

        if len(upcoming_generation)>=3:
            for index in range(0, len(upcoming_generation)-1, 2):
                upcoming_generation[index].geneticly_merge_ticket(upcoming_generation[index+1], max_ticket_price)


            print("Mutating Tickets")
            if len(upcoming_generation)>1000:
                # don't mutate all, mutation is very deadly.
                for ticket in upcoming_generation[0:500]:
                      ticket.mutate_ticket(.1)

            # children, otherwise pop shrinks too fast
            if len(upcoming_generation)<len(tickets)+500:
                children = []
                for ticket in upcoming_generation:
                    children.append(copy.deepcopy(ticket))

                upcoming_generation.extend(children)



        else:
            print("Not enough tickets left for genetic activity")
            break
        sys.stdout.flush()

    histo = {}
    for winner in winners[max(winners.keys())]:
        if winner in histo.keys():
            histo[winner] += 1
        else:
            histo[winner] = 1

    d_descending = OrderedDict(sorted(histo.items(),
                                      key=lambda x: x[1], reverse=False))

    for winner, occurance in d_descending.items():
        print("------{0}------".format(occurance))
        print(winner)
        print("Ticket Price: {0}".format(winner.price()))
        #print(player)
        print("Payoff range " + str(md_keno.possible_pay_off_for_ticket_per_game(winner)))
        print("-----")


    # for winner in winners[max(winners.keys())]:
    #     print("------Good Game------")
    #     print(winner)
    #     print("Ticket Price: {0}".format(winner.price()))
    #     #print(player)
    #     print("-----")
    #     print(md_keno.possible_pay_off_for_ticket_per_game(winner))




if __name__ == "__main__":
    run()