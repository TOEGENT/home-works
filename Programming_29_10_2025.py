from datetime import datetime
from abc import ABC,abstractmethod


class Printable:
    @abstractmethod
    def print_info(self):
        pass


class Book(Printable):
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = int(year)

    @property
    def age(self):
        return datetime.now().year - self.year

    def __str__(self):
        return self.info()

    def __eq__(self, other):
        return isinstance(Book, other) and self.title == other.title

    def print_info(self):
        return f"Title: {self.title}, author: {self.author}, year: {self.year}"

    @classmethod
    def book_init(cls, string):
        l = string.split(";")
        title = l[0]
        author = l[1]
        year = l[2]
        return cls(title, author, year)


book1 = Book.book_init("Пушкин;Евгений Онегин;2020")
print(book1.age)
