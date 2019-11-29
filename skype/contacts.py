import itertools as it_

from skpy import SkypeContacts, SkypeContact, SkypeChats

from channel.contacts import Contact, AddressBook


class SkypeChannelContact(Contact):
    def id(self):
        return self.contact.id

    def __init__(self, contact: SkypeContact):
        self.contact = contact


class SkypeAddressBook(AddressBook):
    def __init__(self, contacts: SkypeContacts, chats: SkypeChats):
        super().__init__()
        for c in it_.chain(contacts, chats):
            self.contacts[c.id] = SkypeChannelContact(c)
