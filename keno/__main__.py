# coding=utf-8
"""
Code to allow launching module directly with python -m keno
"""
from keno.game_runner import GameRunner
def run():
    runner = GameRunner(50)
    runner.run()
