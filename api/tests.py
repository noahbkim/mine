from django.test import TestCase
import timeit

from api.schema import schema


class PerformanceTestCase(TestCase):
    """Check performance of querying the database."""

    def test_query(self):
        """Test the base query speed."""

        def query():
            schema.execute("query { items { id } }")

        timeit.timeit(query, number=1000)
