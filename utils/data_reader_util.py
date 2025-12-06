import json


def read_all_coffee_details_from_file(file_path):
    """
    Read test data from a JSON file and return coffee details of certain coffee name.
    Example JSON structure:
    [{"name": "Espresso","name_chinese" : "特浓咖啡","price": 10,"composition": [{"espresso": 30}]}]
    """
    file = open(file_path, "r", encoding="utf8")
    all_coffee_details = json.load(file)
    return all_coffee_details


def get_coffee_item_details_by_name(all_coffee_details, coffee_name):
    coffee_details = [coffee_details for coffee_details in all_coffee_details
                      if coffee_details["name"] == coffee_name]
    if len(coffee_details) < 1:
        raise Exception("Coffee details for [" + coffee_name + "] not found. Please, check test data file.")
    if len(coffee_details) > 1:
        raise Exception("Found duplicate coffee details for [" + coffee_name + "]. Please, check test data file.")
    return coffee_details[0]
