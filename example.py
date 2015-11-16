__author__ = 'baranbartu'
from memgraph.decorator import observe


@observe(precision=5)
def test_memory():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


if __name__ == '__main__':
    test_memory()
