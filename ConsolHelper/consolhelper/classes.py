from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime
from birthdays import get_birthdays
from re import match

class Field: #?
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field): #?
	pass

class Phone(Field):
    def __init__(self, value):
        pattern = r"^\+?(\d{2})?(0\d{2})(\d{7})$"
        if not match(pattern, value):
            raise ValueError("Invalid phone number format")
        super().__init__(value) #?
        self.value = value #?
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
                 
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
    
    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"{self.name.value} - {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        del self.data[name]
        
    def get_upcoming_birthdays(self):
        return get_birthdays(self)
        
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())
    

class View(ABC):
    @abstractmethod
    def display_contacts(self, record):
        pass
    
    @abstractmethod
    def display_message(self, message):
        pass
    
    @abstractmethod
    def display_commands(self):
        pass


class ConsoleView(View):
    def display_contacts(self, record):
        print("*****")
        for record in record:
            print(f"Name: {record.name.value} | "
                f"Phone: {'; '.join(p.value for p in record.phones)} | "
                f"Birthday: {record.birthday.value.strftime('%d.%m.%Y') if record.birthday else 'No birthday'}")
            print("=====")

    def display_message(self, message):
        print(message)
        
    def display_commands(self):
            print(
            "hello - Greet the user",
            "add <name> <phone> - Add a new contact or update an existing one",
            "change <name> <new_phone> - Change a contact's number",
            "phone <name> - Show contact's phone",
            "all - Show all contacts",
            "add-birthday <name> <birthday> - Add a birthday to an existing contact",
            "birthday <name> - Show a contact's birthday",
            "upcoming - Show upcoming birthdays for the next 7 days",
            "random - Show a random number and birthday",
            "close - Exit the program", 
            "help - Show all valid commands", sep='\n')