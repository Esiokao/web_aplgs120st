import random
import string


def randChar(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
