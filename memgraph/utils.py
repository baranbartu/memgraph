__author__ = 'baranbartu'

import string
import random


def generate_file_name(chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(6))
