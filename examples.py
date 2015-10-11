from memgraph import observe


@observe
def extend_dict():
    d = {}
    for _ in xrange(1000000):
        d[_] = 'value_%d' % _


extend_dict()
