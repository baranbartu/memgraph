import mock
from unittest import TestCase
from memgraph import observe


class ObserveTestCase(TestCase):
    def test_observe(self):
        func = mock.Mock(return_value=True)
        # todo should be used mock.patch for time.sleep
        func.__name__ = 'wait_during_ten_seconds'
        wrapped = observe(func)
        self.assertTrue(wrapped())
        self.assertEquals(func.call_count, 1)
