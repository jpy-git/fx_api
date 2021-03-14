import requests
import json
import pandas as pd
from datetime import datetime as dt
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
from fx_api.helpers import is_string_or_list_of_strings

class FX:
    """FX class allows user to specify source and target currencies when initialising an instance. Various methods can then be applied to obtain desired exchange rates.

    Class Attributes
    -------
    base_url : str
        URL of exchangeratesapi.io
    limits_calls : int, optional
        number of calls permitted in limits_period before rate-limiting begins, by default 20
    limits_period : int, optional
        number of seconds before limits_calls count is reset, by default 20
    limits_max_tries : int, optional
        number of tries before exponential backoff ends and returns RateLimitException, by default 10

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

    # rate limiting params
    limits_calls = 20
    limits_period = 20
    limits_max_tries = 10

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

    @on_exception(expo, RateLimitException, max_tries=limits_max_tries)
    @limits(calls=limits_calls, period=limits_period)
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

            # Check for and raise HTTP exceptions
            response.raise_for_status()

            # Normalize results of JSON response and add to a temporary (source_currency specific) pandas DataFrame
            temp_FX_df = pd.json_normalize(response.json()).rename(columns={"base": "source_currency"})
            
            temp_FX_df = temp_FX_df.melt(
                id_vars=["date", "source_currency"], 
                value_vars=[col for col in temp_FX_df.columns if col.startswith("rates.")], 
                var_name="target_currency", 
                value_name='exchange_rate_to_target'
            )

            temp_FX_df[["target_currency"]] = temp_FX_df["target_currency"].str.split(".", expand=True).loc[:,[1]]
            temp_FX_df = temp_FX_df.loc[:, ["date", "source_currency", "target_currency", "exchange_rate_to_target"]]

            # Append temporary (source_currency specific) pandas DataFrame to master pandas DataFrame to return complete result
            FX_df = FX_df.append(
                temp_FX_df, 
                ignore_index=True
            )

        FX_df.sort_values(
            by=["date", "source_currency", "target_currency"],
            ascending=True,
            inplace=True
        )
        
        FX_df.reset_index(
            drop=True, 
            inplace=True
        )

        return FX_df

    @on_exception(expo, RateLimitException, max_tries=limits_max_tries)
    @limits(calls=limits_calls, period=limits_period)
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

            # Check for and raise HTTP exceptions
            response.raise_for_status()

            # Normalize results of JSON response and add to a temporary (source_currency specific) pandas DataFrame
            temp_FX_df = pd.json_normalize(response.json()).rename(columns={"base": "source_currency"})
            
            temp_FX_df = temp_FX_df.melt(
                id_vars=["date", "source_currency"], 
                value_vars=[col for col in temp_FX_df.columns if col.startswith("rates.")], 
                var_name="target_currency", 
                value_name='exchange_rate_to_target'
            )

            temp_FX_df[["target_currency"]] = temp_FX_df["target_currency"].str.split(".", expand=True).loc[:,[1]]
            temp_FX_df = temp_FX_df.loc[:, ["date", "source_currency", "target_currency", "exchange_rate_to_target"]]

            # Append temporary (source_currency specific) pandas DataFrame to master pandas DataFrame to return complete result
            FX_df = FX_df.append(
                temp_FX_df, 
                ignore_index=True
            )

        FX_df.sort_values(
            by=["date", "source_currency", "target_currency"],
            ascending=True,
            inplace=True
        )
        
        FX_df.reset_index(
            drop=True, 
            inplace=True
        )

        return FX_df

    @on_exception(expo, RateLimitException, max_tries=limits_max_tries)
    @limits(calls=limits_calls, period=limits_period)
    def get_FX_date_range(self, start_at, end_at):
        """Retrieve pandas DataFrame of exchange rates for within specified date range

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

            # Check for and raise HTTP exceptions
            response.raise_for_status()
            
            # Normalize results of JSON response and add to a temporary (source_currency specific) pandas DataFrame
            temp_FX_df = pd.json_normalize(response.json()).rename(columns={"base": "source_currency"})
            
            temp_FX_df = temp_FX_df.melt(
                id_vars=["source_currency"], 
                value_vars=[col for col in temp_FX_df.columns if col.startswith("rates.")], 
                var_name="target_currency", 
                value_name='exchange_rate_to_target'
            )

            temp_FX_df[["date", "target_currency"]] = temp_FX_df["target_currency"].str.split(".", expand=True).loc[:,[1, 2]]
            temp_FX_df = temp_FX_df.loc[:, ["date", "source_currency", "target_currency", "exchange_rate_to_target"]]

            # Append temporary (source_currency specific) pandas DataFrame to master pandas DataFrame to return complete result
            FX_df = FX_df.append(
                temp_FX_df, 
                ignore_index=True
            )

        FX_df.sort_values(
            by=["date", "source_currency", "target_currency"],
            ascending=True,
            inplace=True
        )
        
        FX_df.reset_index(
            drop=True, 
            inplace=True
        )

        return FX_df