"""Test for pretty format table from jsons."""

from tabulate import tabulate
from ecs_tasks_ops import pretty_table


def test_tabulate_list_json_empty():
    out = pretty_table.tabulate_list_json()
    assert "No data to show" == out


def test_tabulate_list_json_empty_msg():
    empty_msg = "No information"
    out = pretty_table.tabulate_list_json(empty_msg=empty_msg)
    assert empty_msg == out


def test_tabulate_list_json_data():
    data = [{"foo": 1, "bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json(data)
    assert tabulate(data, headers={"foo": "foo", "bar": "bar", "none": "none"}) == out


def test_tabulate_list_json_only_one():
    data = [{"foo": 1, "bar": "hi", "none": None}]
    data_test = [{"foo": 1}]
    out = pretty_table.tabulate_list_json(data, fields_to=1)
    assert tabulate(data_test, headers={"foo": "foo"}) == out


def test_tabulate_list_json_from_one_to_three():
    data = [{"foo": 1, "bar": "hi", "none": None}]
    data_test = [{"bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json(data, fields_from=1, fields_to=3)
    assert tabulate(data_test, headers={"bar": "bar", "none": "none"}) == out


def test_tabulate_list_json_from_out_of_index():
    data = [{"foo": 1, "bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json(data, fields_from=4)
    assert '' == out


def test_tabulate_list_json_from_out_of_index():
    data = [{"foo": 1, "bar": "hi", "none": None}]
    out = pretty_table.tabulate_list_json(data, fields_to=4)
    assert tabulate(data, headers={"foo": "foo", "bar": "bar", "none": "none"}) == out
