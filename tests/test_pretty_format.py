"""Test for pretty format table from jsons."""
from datetime import datetime

from tabulate import tabulate

from ecs_tasks_ops import pretty_json
from ecs_tasks_ops import pretty_table


def test_tabulate_list_json_empty():
    """Test empty data."""
    out = pretty_table.tabulate_list_json()
    assert "No data to show" == out


def test_tabulate_list_json_empty_msg():
    """Test empty data with empty msg."""
    empty_msg = "No information"
    out = pretty_table.tabulate_list_json(empty_msg=empty_msg)
    assert empty_msg == out


def test_tabulate_list_json_data():
    """Test all data tabulation."""
    data = [{"foo": 1, "bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json(data)
    assert tabulate(data, headers={"foo": "foo", "bar": "bar", "none": "none"}) == out


def test_tabulate_list_json_only_one():
    """Test only first attribute data tabulation."""
    data = [{"foo": 1, "bar": "hi", "none": None}]
    data_test = [{"foo": 1}]
    out = pretty_table.tabulate_list_json(data, fields_to=1)
    assert tabulate(data_test, headers={"foo": "foo"}) == out


def test_tabulate_list_json_from_one_to_three():
    """Test from one to there (no inclusive) attribute data tabulation."""
    data = [{"foo": 1, "bar": "hi", "none": None}]
    data_test = [{"bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json(data, fields_from=1, fields_to=3)
    assert tabulate(data_test, headers={"bar": "bar", "none": "none"}) == out


def test_tabulate_list_json_from_out_of_index():
    """Test out of index tabulation."""
    data = [{"foo": 1, "bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json(data, fields_from=4)
    assert "" == out


def test_tabulate_list_json_to_out_of_index():
    """Test out of index tabulation."""
    data = [{"foo": 1, "bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json(data, fields_to=4)
    assert tabulate(data, headers={"foo": "foo", "bar": "bar", "none": "none"}) == out


def test_tabulate_list_json_keys():
    """Test tabulation where you can specify keys."""
    data = [{"foo": 1, "bar": "hi", "none": None}]
    data_test = [{"foo": 1, "none": None}]
    out = pretty_table.tabulate_list_json_keys(data, keys=["foo", "none"])
    assert tabulate(data_test, headers={"foo": "foo", "none": "none"}) == out


def test_tabulate_list_json_keys_non_exists():
    """Test tabulation where you can specify keys, but that keys don't exists."""
    data = [{"foo": 1, "bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json_keys(data, keys=["another", "no_included"])
    assert "" == out


def test_json_object_date():
    """Testing a json code with datetime."""
    now = datetime.now()
    data = [{"name": "Object name", "date": now}]
    out = pretty_json.dumps(data, indent=None)
    assert out == '[{"name": "Object name", "date": "' + now.isoformat() + '"}]'


def test_encoder_not_date():
    """Testing a encoder object not date."""
    now = datetime.now()
    dte = pretty_json.DateTimeEncoder()
    out = dte.default(now)
    assert out == now.isoformat()
    out = dte.default(34)
    assert out is None
