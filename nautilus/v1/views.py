import datetime
import json

import pandas as pd
import requests
import yfinance as yf
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class StockViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        """
        request: incoming request with query params interval =  x where
                 x in ['5D', '60D', 'YTD', '1Y', '2Y']
        pk: Ticker/company name of the stock

        Given Ticker/company name, retrive stock data for the given interval

        return:
            Response with status = 400 and error msg if data is empty for the Ticker
            Response with status = 200 and stock data if data retrieved successfully

            The return data looks like following:
            {
                data: {
                    name: S&P 500(^GSPC),
                    50DSMA: [4366.11, 4288.28, 4293.62],
                    200DSMA: ['', 4357.94, 4374.35],
                    columns: ['Open', 'Close', 'Low', 'High'],
                    data: [
                        [3891.99, 3898.81, 3885.73, 3917.35],
                        [3915.54, 3900.34, 3815.54, 3960.27],
                        [3924.52, 3943.34, 3915.21, 3944.99]
                    ],
                    index: ['2021-03-10', '2021-03-11', '2021-03-12'],
                    volume: [
                        [0, 5847380000, -1],
                        [1, 5312880000, 1],
                        [2, 4476280000, -1]
                    ]
                }
            }

            Where 50DSMA and 200DSMA represents 50/200 days simple moving average,
            data represents daily OCLH for the stock,
            volume represents [index, volume, 1 if (today's open > today's close) else -1]

        """
        try:
            ticker, name, time_format, hist = self._get_hist(pk, request.query_params.get("interval"))
        except ValueError:
            return Response(data={"data": []})
        else:
            self._simple_moving_average(hist, 50)
            self._simple_moving_average(hist, 200)

            hist["Volume"] = hist.apply(
                lambda x: [x["Volume"], 1]
                if x["Open"] > x["Close"]
                else [x["Volume"], -1],
                axis=1,
            )

            data = hist[["Open", "Close", "Low", "High"]].round(2).copy()
            json_format_data = data.to_json(orient="split", date_format="epoch")
            result = json.loads(json_format_data)
            result["name"] = name + " (" + ticker + ")"
            result["index"] = [
                datetime.datetime.fromtimestamp(x / 1000.0).strftime(time_format)
                for x in result["index"]
            ]
            result["50DSMA"] = pd.Series(hist["50D-SMA"]).fillna("").tolist()
            result["200DSMA"] = pd.Series(hist["200D-SMA"]).fillna("").tolist()
            result["volume"] = [
                [idx, item[0], item[1]]
                for idx, item in enumerate(pd.Series(hist["Volume"]).tolist())
            ]

            return Response(data=result)

    @action(detail=True, methods=['get'])
    def close(self, request, pk=None):
        """
        request: incoming request with query params interval =  x where
                 x in ['5D', '60D', 'YTD', '1Y', '2Y']
        pk: Ticker/company name of the stock

        Given Ticker/company name, retrive stock data for the given interval.
        Only show close data for each day.

        return:
            Response with status = 400 and error msg if data is empty for the Ticker
            Response with status = 200 and stock data if data retrieved successfully

            The return data looks like following:
            {
                data: {
                    name: S&P 500(^GSPC),
                    ticker: ^GSPC,
                    data: [3898.81, 3900.34, 3943.34]
                }
            }
            where close represents the close prices of the stock
        """
        try:
            ticker, name, _ , hist = self._get_hist(pk, request.query_params.get("interval"))
        except ValueError:
            return Response(data={"data": []})
        else:
            result = {}
            result["name"] = name + " (" + ticker + ")"
            result["ticker"] = ticker
            result["data"] = pd.Series(hist["Close"]).round(2).tolist()

            return Response(data=result)

    def _simple_moving_average(self, data, time_period):
        """
        data: pandas.dataframe, represents the history data of a stock.
              data must contains a column 'Close'
        time_period: int, represents the time periods for moving average.

        Calculate the moving average for a stock,
        and add a new column `${time_period}D-SMA` to the data frame.

        return: no return value, the data is mutated.
        """
        data[str(time_period) + "D-SMA"] = (
            data["Close"].rolling(window=time_period).mean().round(2)
        )

    def _get_info(self, id):
        """
        id: company's name or ticker symbols

        find the corresponding stock given ticker or company's name

        return (ticker, company name)
        """
        yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        params = {"q": id, "quotes_count": 1, "country": "United States"}

        res = requests.get(
            url=yfinance, params=params, headers={"User-Agent": user_agent}
        )
        data = res.json()

        company_code = data["quotes"][0]["symbol"]
        company_name = data["quotes"][0]["shortname"]
        return (company_code, company_name)

    def _get_hist(self, id, interval):
        """
        id: company's name or ticker symbols
        interval: history time interval

        Given id and desired time interval, 
        return ticker, company name, time_format, 
        and history data during the time interval
        """
        try:
            ticker, name = self._get_info(id)
        except (KeyError, IndexError):
            raise ValueError
        else:
            time_format = "%Y-%m-%d"
            time_interval = "1d"
            if interval == "5D":
                time_format = "%Y-%m-%d %H:%M"
                time_interval = "5m"
            elif interval == "60D":
                time_format = "%Y-%m-%d %H:%M"
                time_interval = "60m"

            stock = yf.Ticker(ticker)
            hist = stock.history(period=interval, interval=time_interval)

            if hist.empty:
                raise ValueError
            
            return (ticker, name, time_format, hist)
