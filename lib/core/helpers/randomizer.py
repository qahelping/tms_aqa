from random import choice, randint

import rstr

from lib.monolith.constants import PASSWORD_PATTERN_STRONG


class Randomizer:

    @staticmethod
    def choice(options):
        return choice(options)

    @staticmethod
    def generate_float(length):
        return (randint(10 ** (length - 1), 10 ** length - 1)) / (10 ** length)

    @staticmethod
    def generate_id(length=8):
        return str(Randomizer.generate_int(length))

    @staticmethod
    def generate_int(length):
        return randint(10 ** (length - 1), 10 ** length - 1)

    @staticmethod
    def generate_password(pattern=PASSWORD_PATTERN_STRONG):
        return Randomizer.generate_string_matching_regex(pattern)

    @staticmethod
    def generate_string_matching_regex(pattern):
        return rstr.xeger(pattern)

    @staticmethod
    def randint(first_int, last_int):
        return randint(first_int, last_int)
