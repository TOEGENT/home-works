class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return self.info()

    def __eq__(self, other):
        return isinstance(Book, other) and self.title == other.title

    def info(self):
        return f"Title: {self.title}, author: {self.author}, year: {self.year}"

    @classmethod
    def book_init(cls, string):
        l = string.split(";")
        title = l[0]
        author = l[1]
        year = l[2]
        return cls(title, author, year)


book1 = Book.book_init("Пушкин;Евгений Онегин;2020")
print(book1)
