from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self):
        return f'{self.value}'


class Name(Field):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone: str) -> None:
        super().__init__(phone)
        self.__phone = None
        self.value = phone

    def __repr__(self) -> str:
        return str(self)

    @property
    def value(self):
        return self.__phone

    @value.setter
    def value(self, phone):
        normalized_phone = (
            phone.strip()
            .replace("+", "")
            .replace("-", "")
            .replace(" ", "")
            .replace(")", "")
            .replace("(", "")
        )
        if len(normalized_phone) == 12:
            if normalized_phone.isdigit():
                self.__phone = normalized_phone
            else:
                raise ValueError('Wrong phone format')
        else:
            raise ValueError('Wrong phone format')


class Birthday(Field):
    def __init__(self, birthday: str) -> None:
        super().__init__(birthday)
        self.__birthday = None
        self.value = birthday

    @property
    def value(self):
        return self.__birthday

    @value.setter
    def value(self, birthday):
        norm_birthday = (
            birthday.strip()
            .replace(" ", "-")
            .replace("/", "-")
            .replace(".", "-")
        )
        try:
            self.__birthday = datetime.strptime(
                norm_birthday, '%d-%m-%Y').date()
        except:
            try:
                self.__birthday = datetime.strptime(
                    norm_birthday, '%Y-%m-%d').date()
            except:
                raise ValueError('Wrond date format')


class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phones(self):
        self.phones.clear()

    def change_phones(self, phone: Phone):
        self.phones = [phone]

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        today = datetime.now().date()
        birthdate = self.birthday.value.replace(year=today.year)
        delta = birthdate - today
        if delta.days >= 0:
            return delta.days
        else:
            birthdate.replace(year=today.year+1)
            delta = birthdate - today
            return delta.days

    def __str__(self) -> str:
        return f'Contact Name: {self.name}, Phones: {self.phones if self.phones else "None"}, Birthday: {self.birthday}'

    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        self.N_records = None
        self.index = 0

    def iterator(self, N):
        self.n = N
        self.count = 0
        self.start = 0
        while True:
            result = f'Page {self.count // self.n + 1} of {len(self.data) // self.n + 1}'
            for i in range(self.start, self.start+self.n):
                if self.count == len(self.data):
                    raise StopIteration
                result += f'\n{list(self.data.values())[i]}'
                self.count += 1
            yield result
            input('Press any key to continue: ')
            self.start += self.n

    def __str__(self) -> str:
        return '\n'.join(str(record) for record in self.data.values())

    def __repr__(self) -> str:
        return str(self)


address_book = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
        except TypeError:
            result = 'Missing contact name or phone or date'
        except UnboundLocalError:
            result = 'Unknown command'
        except ValueError:
            result = 'Wrong phone format'
        except KeyError:
            result = f'Name: {args[0]} not in address book'
        return result
    return inner


def unknown_command(command: str) -> str:
    return f'Unknown command "{command}"'


def hello_user(*args) -> str:
    return 'How can I help you?'


def exit_func(*args) -> str:
    return 'Goodbye!'


@input_error
def contact_adder(name: str, phone=None) -> str:
    if name in address_book.data.keys():
        return f'Contact Name: {name} already exists'

    record_name = Name(name)
    record = Record(record_name)

    if phone:
        record_phone = Phone(phone)
        record.add_phone(record_phone)

    address_book.add_record(record)

    return f'Added contact Name: {record.name} with Phone: {record.phones if record.phones else "None"}'


@input_error
def phone_adder(name: str, phone: str) -> str:
    record = address_book.data[name]

    for ph in record.phones:
        if ph.value == phone:
            return f'Phone: {phone} for contact Name: {record.name} already exists'

    record_phone = Phone(phone)
    record.add_phone(record_phone)

    return f'Contact Name: {record.name} new Phones: {record.phones}'


@input_error
def birthday_adder(name: str, birthday: str) -> str:
    record = address_book.data[name]

    if record.birthday:
        return f'Contact Name: {record.name} already has Birthday: {record.birthday}'
    else:
        record_birthday = Birthday(birthday)
        record.add_birthday(record_birthday)
        return f'Contact Name: {record.name}, Birthday: {record.birthday} is added'


@input_error
def phones_remover(name: str) -> str:
    record = address_book.data[name]

    record.remove_phones()
    return f'{record}'


@input_error
def phone_changer(name: str, phone: str) -> str:
    record = address_book.data[name]

    record_phone = Phone(phone)
    record.change_phones(record_phone)
    return f'Contact Name: {record.name} has new Phone: {record.phones}'


@input_error
def birthday_changer(name: str, birthday: str) -> str:
    record = address_book.data[name]

    record_birthday = Birthday(birthday)
    record.add_birthday(record_birthday)
    return f'Contact Name: {record.name}, Birthday: {record.birthday} is updated'


@input_error
def contact_displayer(name: str) -> str:
    record = address_book.data[name]
    if record.birthday:
        return f'{record}\nDays to birthday - {record.days_to_birthday()}'
    else:
        return f'{record}'


@input_error
def show_all() -> str:
    if address_book.data:
        N = input('How many contacts to show? ')
        print(f'Showing all contacts')
        result = address_book.iterator(N)
    else:
        result = 'No contacts, please add'
    return result


commands = {
    'hello': hello_user,
    'add contact': contact_adder,
    '+c': contact_adder,
    'add phone': phone_adder,
    '+p': phone_adder,
    'change phone': phone_changer,
    'remove phones': phones_remover,
    'show all': show_all,
    'show contact': contact_displayer,
    '?c': contact_displayer,
    'exit': exit_func,
    'goodbye': exit_func,
    'good bye': exit_func,
    'close': exit_func,
    'add birthday': birthday_adder,
    '+b': birthday_adder,
    'change birthday': birthday_changer
}


def main():
    while True:
        phrase = input('Please enter request: ').strip()
        command = None
        for key in commands:
            if phrase.lower().startswith(key):
                command = key
                break

        if not command:
            result = unknown_command(phrase.split(' ', 1)[0])
        else:
            data = phrase[len(command):].strip()
            if data:
                if ', ' in data:
                    data = data.split(', ', 1)
                else:
                    data = data.rsplit(' ', 1)

            handler = commands.get(command)
            result = handler(*data)
            if result == 'Goodbye!':
                print(result)
                break
        print(result)


if __name__ == '__main__':
    main()
