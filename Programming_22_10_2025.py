class Book:
    def __init__(self,title,author,year):
        self.title=title
        self.author=author
        self.year=year

    def info(self):
        return f"Title: {self.title}, author: {self.author}, year: {self.year}"

book=Book("Auoroa","ME",2025)

class BankAccount:
    def __init__(self,balance):
        self.balance=balance
    def __deposit(self,amount):
        if amount>0:
            self.balance+=amount
    def get_balance(self):
        return self.balance
account = BankAccount(1000)
account.balance+=500
print(BankAccount.__deposit(500))
@property
class Ebook(Book):
    def __init__(self,format,):
        super().__init__()
        self.format=format
    def info(self):
        return f"Title: {self.title}, author: {self.author}, year: {self.year}, format: {self.format}"


