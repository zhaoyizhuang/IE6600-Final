import numpy as np
import pandas as pd
from django.test import Client, TestCase
from pandas.testing import assert_series_equal
from v1.views import StockViewSet

client = Client()


class StockViewSetTestCase(TestCase):
    def test_empty_ticker_data(self):
        response = client.get("/stock/^GSPC3", {"interval": "5D"}, follow=True)

        assert response.status_code == 200
        assert response.data == {"data": []}

    def test_successfully_retrieve_data(self):
        response = client.get("/stock/^GSPC", {"interval": "5D"}, follow=True)

        assert response.status_code == 200

    def test_simple_moving_average(self):
        view_set = StockViewSet()
        data = [10, 20, 30, 40, 50, 70]
        df = pd.DataFrame(data, columns=["Close"])
        view_set._simple_moving_average(df, 3)

        expected_df = pd.DataFrame({"3D-SMA": [np.nan, np.nan, 20, 30, 40, 53.33]})
        assert_series_equal(df["3D-SMA"], expected_df["3D-SMA"])

    def test_get_info(self):
        view_set = StockViewSet()
        assert view_set._get_info("^GSPC") == ("^GSPC", "S&P 500")
        assert view_set._get_info("S&P 500") == ("^GSPC", "S&P 500")

    def test_get_hist(self):
        view_set = StockViewSet()
        self.assertRaises(ValueError, view_set._get_hist, "qweqwe", "2Y")
        self.assertRaises(ValueError, view_set._get_hist, "", "2Y")

