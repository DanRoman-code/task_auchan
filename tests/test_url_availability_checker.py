from unittest import TestCase
from url_availability_checker import UrlAvailabilityChecker


class TestUrlAvailabilityChecker(TestCase):

    def test_200_status_code(self):
        actual = UrlAvailabilityChecker([]).get_status_code("https://www.google.com/")
        self.assertEqual(actual, 200)

    def test_404_status_code(self):
        actual = UrlAvailabilityChecker([]).get_status_code("https://www.google.com/asfasg/")
        self.assertEqual(actual, 404)

    def test_chech_unshorten_url_work(self):
        actual = UrlAvailabilityChecker([]).get_unshorten_url("http://ow.ly/qTP050gW0F9")
        self.assertEqual(
            actual,
            "https://www.clinicaltrialsarena.com/uncategorized/overcoming-operational-barriers-to-implementing-ecoa-in-a-clinical-trial-6089276-2/"
        )
