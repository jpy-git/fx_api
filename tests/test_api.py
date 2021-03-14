import pytest
from fx_api import FX
from datetime import date, timedelta, datetime
import requests

def test_base_url():
    """Test base_url points to exchangeratesapi.io
    """
    assert FX.base_url == "https://api.exchangeratesapi.io"

def test_default_init():
    """Test to verify default instance attributes
    """
    fx = FX()
    assert [fx.source_currency, fx.target_currency] == [["GBP"], None]

def test_init():
    """Test to verify user set instance attributes
    """
    fx = FX(
        source_currency=["USD", "GBP", "EUR"],
        target_currency=["JPY", "CAD"]
    )
    assert [fx.source_currency, fx.target_currency] == [["USD", "GBP", "EUR"], ["JPY", "CAD"]]

def test_init_source_fail():
    """Test non str/list of str inputs of source_currency raise TypeError
    """
    with pytest.raises(TypeError):
        fx = FX(
            source_currency=["USD", "GBP", 567]
        )

def test_init_target_fail():
    """Test non str/list of str/None inputs of target_currency raise TypeError
    """
    with pytest.raises(TypeError):
        fx = FX(
            target_currency=["JPY", True]
        )

def test_get_FX_latest_non_empty():
    """Test returned DataFrame is non empty
    """
    assert FX().get_FX_latest().shape[0] > 0

def test_get_FX_latest_date():
    """Test returned date is in last week (could be that today not yet updated or is not a working day)
    """
    today = datetime.today()
    last_week = today - timedelta(days=7)
    assert datetime.strptime(FX().get_FX_latest()['date'][0], '%Y-%m-%d') > last_week 
    assert datetime.strptime(FX().get_FX_latest()['date'][0], '%Y-%m-%d') <= today

def test_get_FX_latest_type():
    """Test dtypes of returned DataFrame
    """
    assert FX().get_FX_latest().dtypes.apply(lambda x: x.name).to_dict() == {'date': 'object', 'source_currency': 'object', 'target_currency': 'object', 'exchange_rate_to_target': 'float64'}

def test_get_FX_latest_HTTPError():
    """Test HTTPException raised on bad query
    """
    with pytest.raises(requests.HTTPError):
        FX(source_currency='ads').get_FX_latest()

def test_get_FX_date_non_empty():
    """Test returned DataFrame is non empty
    """
    assert FX().get_FX_date(date="2019-07-23").shape[0] > 0

def test_get_FX_date_date():
    """Test returned date is same as input date
    """
    assert FX().get_FX_date(date="2020-03-13")['date'][0] == "2020-03-13"

def test_get_FX_date_type():
    """Test dtypes of returned DataFrame
    """
    assert FX().get_FX_date(date="2020-07-01").dtypes.apply(lambda x: x.name).to_dict() == {'date': 'object', 'source_currency': 'object', 'target_currency': 'object', 'exchange_rate_to_target': 'float64'}

def test_get_FX_date_type_fail():
    """Test non str inputs of date raise TypeError
    """
    with pytest.raises(TypeError):
        FX().get_FX_date(date=2019)

def test_get_FX_date_value_fail():
    """Test non "YYYY-MM-DD" format inputs of date raise ValueError
    """
    with pytest.raises(ValueError):
        FX().get_FX_date(date="2019-07-63")

def test_get_FX_date_range_non_empty():
    """Test returned DataFrame is non empty
    """
    assert FX().get_FX_date_range(start_at="2019-07-23", end_at="2019-07-29").shape[0] > 0

def test_get_FX_date_range_date():
    """Test returned dates are subset of input dates
    N.B. wouldn't expect full match as history only updated on working days
    """
    assert set(FX().get_FX_date_range(start_at="2020-03-14", end_at="2020-03-17")['date'].unique().tolist()) <= set(["2020-03-14", "2020-03-15", "2020-03-16", "2020-03-17"])

def test_get_FX_date_range_type():
    """Test dtypes of returned DataFrame
    """
    assert FX().get_FX_date_range(start_at="2020-07-01", end_at="2020-07-06").dtypes.apply(lambda x: x.name).to_dict() == {'date': 'object', 'source_currency': 'object', 'target_currency': 'object', 'exchange_rate_to_target': 'float64'}

def test_get_FX_date_range_start_type_fail():
    """Test non str inputs of start_at raise TypeError
    """
    with pytest.raises(TypeError):
        FX().get_FX_date_range(start_at=123, end_at="2020-03-17")

def test_get_FX_date_range_start_value_fail():
    """Test non "YYYY-MM-DD" format inputs of start_at raise ValueError
    """
    with pytest.raises(ValueError):
        FX().get_FX_date_range(start_at="2020-032-01", end_at="2020-03-17")

def test_get_FX_date_range_end_type_fail():
    """Test non str inputs of end_at raise TypeError
    """
    with pytest.raises(TypeError):
        FX().get_FX_date_range(start_at="2020-03-14", end_at=False)

def test_get_FX_date_range_end_value_fail():
    """Test non "YYYY-MM-DD" format inputs of end_at raise ValueError
    """
    with pytest.raises(ValueError):
        FX().get_FX_date_range(start_at="2020-03-14", end_at="2020-03-176")


