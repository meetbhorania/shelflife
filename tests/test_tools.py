from types import SimpleNamespace

from shelflife.tools import book_collection, find_nearby_charities, read_surplus_list


def ctx():
    return SimpleNamespace(state={})


def test_expired_food_is_removed():
    result = read_surplus_list(ctx(), today="2026-10-31")
    removed = {i["item"] for i in result["removed"]}
    assert removed == {"Fruit salad cups", "Egg mayo sandwiches"}
    assert all(i["use_by"] >= "2026-10-31" for i in result["safe"])


def test_charities_are_close_and_accept_the_food():
    result = find_nearby_charities(["bakery"], max_miles=3)
    names = [c["name"] for c in result["charities"]]
    assert "Walthamstow Soup Run" not in names  # only takes ready meals
    assert all(c["miles"] <= 3 for c in result["charities"])


def test_booking_needs_confirmation():
    result = book_collection("c2", "17:30", ["Croissants"], confirmed_by_cafe=False, tool_context=ctx())
    assert result["status"] == "needs_confirmation"


def test_booking_rejects_wrong_slot():
    result = book_collection("c2", "12:00", ["Croissants"], confirmed_by_cafe=True, tool_context=ctx())
    assert result["status"] == "error"
