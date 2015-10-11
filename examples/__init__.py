from memgraph import observe


@observe
def extend_dict():
    d = {}
    for _ in xrange(500):
        d[_] = 'value_%d' % _


print 'Executing extend_dict.'
extend_dict()
print 'Done.'
