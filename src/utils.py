import random
import string


def random_str(k=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))
