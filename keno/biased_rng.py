# coding=utf-8
"""
Attempt to creat an RNG that picks numbers like humans

# favors date parts (1-31, 1-12, 19/20, 50-99/00-18)
# seeks/avoids patterns (i.e. 1,2,3,4,5 or 2,22,32,42)
# favors past winning numbers
# favors culturally meaningful numbers, 777, 888, etc.
"""
import random
from datetime import date, timedelta


class BiasedRng(object):
    """
    Birthday numbers. Simulate what happens if you only pick birthday numbers.
    Against an unbiased state RNG, you expect a higher risk of capped payouts from
    too many people winning, otherwise no change-- all numbers are just as good as
    any other.

    If you were playing keno with friends (and not the state), one player could exploit the fact that
    the other is using a BiasedRng.
    """
    def __init__(self):
        pass

    def dates_only(self):
        """
        Pick number drawn from a biased RNG
        :return:
        """
        pick = set()
        while len(pick) < 20:
            birthday = self.random_birthday()
            pick.update(self.keno_range(birthday))
        pick_list = [x for x in pick]
        pick_list.sort()
        return pick_list

    def random_birthday(self):
        """
        Birthdays for people up to 80 years old.
        :return:
        """
        days = 365 * 80
        oldest_birthday = date.today() - timedelta(days=days)
        days_since_random_birthday = random.randint(0, days)
        return oldest_birthday + timedelta(days=days_since_random_birthday)

    def keno_range(self, value: date):
        """
        Break date into part and return set of parts from 1 to 80
        :param value:
        :return:
        """
        full_range = {int(str(value.year)[0:2]), int(str(value.year)[2:]), value.day, value.month} - {0}
        pick = set()
        for x in full_range:
            if x <= 80:
                pick.add(x)
        return pick


if __name__ == "__main__":
    rng = BiasedRng()
    bday = rng.random_birthday()
    print(bday)
    print(rng.keno_range(bday))
    print(rng.dates_only())
