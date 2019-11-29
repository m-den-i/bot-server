from typing import Dict

from channel.exceptions import ContactNotFoundException


class Contact:
    def id(self):
        raise NotImplementedError()


class AddressBook:
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}

    def find_contact(self, search_term: str) -> Contact:
        if search_term in self.contacts:
            return self.contacts[search_term]

        raise ContactNotFoundException('Contact {} not found'.format(search_term))
