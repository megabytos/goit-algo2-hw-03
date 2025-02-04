from dataclasses import dataclass
from BTrees.OOBTree import OOBTree
import timeit
import csv

tree = OOBTree()
dictionary = {}


@dataclass
class Item:
    ID: int
    Name: str
    Category: str
    Price: float

    def __post_init__(self):
        self.ID = int(self.ID)
        self.Price = float(self.Price)


def load_data(filename):
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        i = 0
        for row in reader:
            item = Item(**row)
            add_item_to_dict(item)
            add_item_to_tree(item)


def add_item_to_tree(item: Item) -> None:
    tree.update({(item.Price, item.ID): item})


def add_item_to_dict(item):
    dictionary[(item.Price, item.ID)] = item


def range_query_tree(start, end):
    return tree.items((start,), (end,))


def range_query_dict(start, end):
    return [value for (price, _), value in dictionary.items() if start <= price <= end]


if __name__ == '__main__':
    load_data('generated_items_data.csv')
    start = 50
    end = 150
    time_tree = timeit.timeit(lambda: range_query_tree(start, end), number=100)
    time_dict = timeit.timeit(lambda: range_query_dict(start, end), number=100)

    print(f"Total range_query time for OOBTree: {time_tree * 1000:.4f} ms")
    print(f"Total range_query time for Dict: {time_dict * 1000:.4f} ms")
