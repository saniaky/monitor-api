import random
import string


def random_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
