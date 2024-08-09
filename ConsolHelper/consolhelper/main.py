from contextlib import contextmanager
from classes import AddressBook, ConsoleView, Record
from serialization import save_data, load_data

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone or birthday in correct formats."
        except IndexError:
            return "Enter the arguments for the command."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return str(e)
    return inner

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    if book.find(name):
        return "This contact already exists."
    record = Record(name)
    book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def remove_contact(args, book):
    name = args[0]
    book.delete(name)
    return "Contact removed."

@input_error
def change_contact(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    try:    
        new_phone = args[1]
        if record.phones:
            record.edit_phone(record.phones[0].value, new_phone)
        return "Contact updated."
    except IndexError:
        return "Enter the new phone number."
       
@input_error
def show_phone(args, book):
    name = args[0]
    return book[name]
   
@input_error 
def show_all(book, view):
    if book.data.values():
        return view.display_contacts(book.data.values())
    return "No contacts are available."

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."
     
@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name} - {record.birthday.value.strftime('%d.%m.%Y')}"
    return "Birthday not found."
    
@input_error
def birthdays(book):
    records = [{"name": record.name.value, "birthday": record.birthday.value.strftime('%d.%m.%Y')} for record in book.values() if record.birthday]
    birthdays_to_show = AddressBook.get_upcoming_birthdays(records)
    if not birthdays_to_show:
        return "No upcoming birthdays."
    return "\n".join([f"{record['name']} - {record['congratulation_date']}" for record in birthdays_to_show])

def random():
    import random
    main_numbers = random.randint(1000000, 9999999)
    start_numbers = random.choice(['063', '+38097', '095', '+38099'])
    date = random.randint(1, 31)
    month = random.randint(1, 12)
    year = random.randint(1900, 2024)
    if date < 10:
        date = f"0{date}"
    if month < 10:
        month = f"0{month}"
    return f"{start_numbers}{main_numbers} | {date}.{month}.{year}"

    
@contextmanager
def record_manager():
    data = load_data()
    try:
        yield data
    finally:
        save_data(data)
    
def main():
    with record_manager() as book:    
        view = ConsoleView()
        view.display_message("Welcome to the assistant bot!")
        
        while True:
            user_input = input("Enter a command: ")
            command, *args = user_input.split()
            
            match command:
                case 'exit' | 'close':
                    view.display_message('Good bye!')
                    break
                case "help" | "commands":
                    view.display_commands()
                case "hello" | "hi":
                    view.display_message("How can I help you?")
                case "add":
                    view.display_message(add_contact(args, book))
                case "remove":
                    view.display_message(remove_contact(args, book))
                case "change": 
                    view.display_message(change_contact(args, book))
                case "phone": 
                    view.display_message(show_phone(args, book))
                case "all":
                    show_all(book, view)
                case "add-birthday":
                    view.display_message(add_birthday(args, book))
                case "birthday":
                    view.display_message(show_birthday(args, book))
                case "upcoming":
                    view.display_message(birthdays(book))
                case "random":
                    view.display_message(random())
                case "secret":
                    view.display_message("Shh! It's a secret :)")                    
                case _:
                    view.display_message("Invalid command")
        
if __name__ == "__main__":
    main()