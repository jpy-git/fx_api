import requests
import json
import pandas as pd
from datetime import datetime as dt
from helpers import is_string_or_list_of_strings

class FX:
    """FX class allows user to specify source and target currencies when initialising an instance. Various methods can the be applied to obtain desired exchange rates.

    Class Attributes
    -------
    base_url : str
        URL of exchangeratesapi.io

    Instance Attributes
    -------
    source_currency: str or list of str
        currency which is to be converted
    target_currency: str or list of str or None
        target for currency being converted

    Methods
    -------
    get_FX_latest():
        retrieve pandas DataFrame of latest available exchange rates
    get_FX_date(date):
        retrieve pandas DataFrame of exchange rates for a specified date
    get_FX_date_range(start_at, end_at):
        retrieve pandas DataFrame of exchange rates for within specified date range
    """

    # URL of exchangeratesapi.io
    base_url = "https://api.exchangeratesapi.io"

    def __init__(self, source_currency="GBP", target_currency=None):
        """Initialise instance of FX class.

        Parameters
        ----------
        source_currency : str or list of str, optional
            currency which is to be converted, by default "GBP"
        target_currency : str or list of str or None, optional
            target for currency being converted, by default None
        """

        # Input validation
        if not is_string_or_list_of_strings(source_currency):
            raise TypeError("source_currency must be a string or a list of strings")
        
        if target_currency:
            if not is_string_or_list_of_strings(target_currency):
                raise TypeError("target_currency must be a string, a list of strings, or None")
        
        # Create instance attributes
        if isinstance(source_currency, str):
            self.source_currency = [source_currency]
        else:
            self.source_currency = source_currency

        if isinstance(target_currency, str):
            self.target_currency = [target_currency]
        else:
            self.target_currency = target_currency

    def get_FX_latest(self):
        """Retrieve pandas DataFrame of latest available exchange rates.

        Returns
        -------
        pandas DataFrame
            DataFrame containing columns date (str), source_currency (str), target_currency (str), and exchange_rate_to_target (float)
        """
        
        # Create url for latest API query
        url = f"{FX.base_url}/latest"

        # Create empty master pandas DataFrame to store results of method
        FX_df = pd.DataFrame(
            columns={
                "date": str,
                "source_currency": str,
                "target_currency": str,
                "exchange_rate_to_target": float
            }
        )

        # API only allows one source_currency to be queried at a time, therefore iterate over list
        for source_currency in self.source_currency:
            
            # Generate params for HTTP request
            params = {
                "base": source_currency,
                "symbols": self.target_currency
            }

            # Execute HTTP request
            response = requests.get(
                url=url,
                params=params
            )

            # Normalize results of JSON response and add to a temporary (source_currency specific) pandas DataFrame
            source_currency_list = []
            date_list = []
            target_currency_list = []
            exchange_rate_to_target_list = []

            for target_currency in response.json()['rates']:

                date_list.append(response.json()['date'])
                source_currency_list.append(response.json()['base'])
                target_currency_list.append(target_currency)
                exchange_rate_to_target_list.append(response.json()['rates'][target_currency])

            temp_FX_df = pd.DataFrame(
                data={
                    "date": date_list,
                    "source_currency": source_currency_list,
                    "target_currency": target_currency_list,
                    "exchange_rate_to_target": exchange_rate_to_target_list
                }
            )

            # Append temporary (source_currency specific) pandas DataFrame to master pandas DataFrame to return complete result
            FX_df = FX_df.append(
                temp_FX_df, 
                ignore_index=True
            )

        return FX_df

    def get_FX_date(self, date):
        """Retrieve pandas DataFrame of exchange rates for a specified date

        Parameters
        ----------
        date : str
            string in date format YYYY-MM-DD

        Returns
        -------
        pandas DataFrame
            DataFrame containing columns date (str), source_currency (str), target_currency (str), and exchange_rate_to_target (float)
        """

        # Input validation
        if not isinstance(date, str):
            raise TypeError("date must be a string in the date format YYYY-MM-DD")
        else: 
            try:
                dt.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("date must be provided in the date format YYYY-MM-DD")
        
        # Create url for date API query
        url = f"{FX.base_url}/{date}"

        # Create empty master pandas DataFrame to store results of method
        FX_df = pd.DataFrame(
            columns={
                "date": str,
                "source_currency": str,
                "target_currency": str,
                "exchange_rate_to_target": float
            }
        )

        # API only allows one source_currency to be queried at a time, therefore iterate over list
        for source_currency in self.source_currency:
            
            # Generate params for HTTP request
            params = {
                "base": source_currency,
                "symbols": self.target_currency
            }

            # Execute HTTP request
            response = requests.get(
                url=url,
                params=params
            )

            # Normalize results of JSON response and add to a temporary (source_currency specific) pandas DataFrame
            source_currency_list = []
            date_list = []
            target_currency_list = []
            exchange_rate_to_target_list = []

            for target_currency in response.json()['rates']:

                date_list.append(date)
                source_currency_list.append(response.json()['base'])
                target_currency_list.append(target_currency)
                exchange_rate_to_target_list.append(response.json()['rates'][target_currency])

            temp_FX_df = pd.DataFrame(
                data={
                    "date": date_list,
                    "source_currency": source_currency_list,
                    "target_currency": target_currency_list,
                    "exchange_rate_to_target": exchange_rate_to_target_list
                }
            )

            # Append temporary (source_currency specific) pandas DataFrame to master pandas DataFrame to return complete result
            FX_df = FX_df.append(
                temp_FX_df, 
                ignore_index=True
            )

        return FX_df

    def get_FX_date_range(self, start_at, end_at):
        """retrieve pandas DataFrame of exchange rates for within specified date range

        Parameters
        ----------
        start_at : str
            string in date format YYYY-MM-DD
        end_at : str
            string in date format YYYY-MM-DD

        Returns
        -------
        pandas DataFrame
            DataFrame containing columns date (str), source_currency (str), target_currency (str), and exchange_rate_to_target (float)
        """

        # Input validation
        if not isinstance(start_at, str):
            raise TypeError("start_at must be a string in the date format YYYY-MM-DD")
        else: 
            try:
                dt.strptime(start_at, '%Y-%m-%d')
            except ValueError:
                raise ValueError("start_at must be provided in the date format YYYY-MM-DD")

        if not isinstance(end_at, str):
            raise TypeError("end_at must be a string in the date format YYYY-MM-DD or None")
        else: 
            try:
                dt.strptime(end_at, '%Y-%m-%d')
            except ValueError:
                raise ValueError("end_at must be provided in the date format YYYY-MM-DD")
        
        # Create url for date range API query
        url = f"{FX.base_url}/history"

        # Create empty master pandas DataFrame to store results of method
        FX_df = pd.DataFrame(
            columns={
                "date": str,
                "source_currency": str,
                "target_currency": str,
                "exchange_rate_to_target": float
            }
        )

        # API only allows one source_currency to be queried at a time, therefore iterate over list
        for source_currency in self.source_currency:
            
            # Generate params for HTTP request
            params = {
                "base": source_currency,
                "symbols": self.target_currency,
                "start_at": start_at,
                "end_at": end_at
            }

            # Execute HTTP request
            response = requests.get(
                url=url,
                params=params
            )

            # Normalize results of JSON response and add to a temporary (source_currency specific) pandas DataFrame
            source_currency_list = []
            date_list = []
            target_currency_list = []
            exchange_rate_to_target_list = []

            for date in response.json()['rates']:
                for target_currency in response.json()['rates'][date]:

                    date_list.append(date)
                    source_currency_list.append(response.json()['base'])
                    target_currency_list.append(target_currency)
                    exchange_rate_to_target_list.append(response.json()['rates'][date][target_currency])

            temp_FX_df = pd.DataFrame(
                data={
                    "date": date_list,
                    "source_currency": source_currency_list,
                    "target_currency": target_currency_list,
                    "exchange_rate_to_target": exchange_rate_to_target_list
                }
            )

            # Append temporary (source_currency specific) pandas DataFrame to master pandas DataFrame to return complete result
            FX_df = FX_df.append(
                temp_FX_df, 
                ignore_index=True
            )

        return FX_df

if __name__=='__main__':   
    print(FX().get_FX_latest())
    print(FX(source_currency="USD").get_FX_latest())
    print(FX(target_currency="CAD").get_FX_latest())
    print(FX(target_currency=["CAD","USD"]).get_FX_latest())
    print(FX(source_currency=["USD","GBP"],target_currency=["CAD","EUR"]).get_FX_latest())
    print(FX(source_currency=["USD","GBP"]).get_FX_date_range(start_at="2020-12-29",end_at="2021-01-05"))
    print(FX(source_currency=["USD","GBP"]).get_FX_date(date="2020-12-29"))
