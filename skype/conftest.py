import os
import pickle
from datetime import datetime, timedelta
from typing import List

import pytest
from skpy import SkypeChats, SkypeContacts, SkypeNewMessageEvent

from settings import BASE_DIR

_dir = os.path.join(BASE_DIR, 'skype/tests')


@pytest.fixture
def skype_contacts() -> SkypeContacts:
    with open(os.path.join(_dir, 'dump/contacts.skpy'), 'rb') as f:
        contacts = pickle.load(f)
    return contacts


@pytest.fixture
def skype_chats() -> SkypeChats:
    with open(os.path.join(_dir, 'dump/chats.skpy'), 'rb') as f:
        chats = pickle.load(f)
    return chats


@pytest.fixture
def skype_mention() -> List[SkypeNewMessageEvent]:
    with open(os.path.join(_dir, 'dump/mention.skpy'), 'rb') as f:
        events = pickle.load(f)
    return events


@pytest.fixture
def fake_token():
    tomorrow = datetime.now() + timedelta(days=1)
    skypeExpiry = tomorrow
    regExpiry = skypeExpiry + timedelta(seconds=1)
    return [
        'live:.cid.3063e944954ae659',
        'eyJhbGciOiJSUzI1NiIsImtpZCI6IjEwMSIsInR5cCI6IkpXVCJ9.eyJpYXQ'
        'iOjE1NzQ3NTYxMTMsImV4cCI6MTU3NDg0MjUxMiwic2t5cGVpZCI6ImxpdmU'
        '6LmNpZC4zMDYzZTk0NDk1NGFlNjU5Iiwic2NwIjo5NTgsImNzaSI6IjE1NzQ'
        '3NTYxMTIiLCJjaWQiOiIzMDYzZTk0NDk1NGFlNjU5IiwiYWF0IjoxNTc0NzU'
        '2MTEyfQ.jDx4mxWmtudun6y5BChR6qa4YYK_YjGkEjKuSoEYoHPm4zROSiG6'
        '9Kuj_Uh5u5iN7iP3Rq8EyKa1bGgv0WAzokOUjBUbYBn-Ktd4YgF6DJfwJqMO'
        '68gI_QCb8u9Bg-KaCrS76pSxmBBIJAaBTVyOU0OLXRlE4x6Ft2F5Aj3EKbTa'
        'C8ex2zlZk-cvQgtBwZoYQwup5yFGauuZV52CYJas7xX_W9fWNr8EVyZcEJNu'
        'fBl68FhXgEIcFajRmlESnX_WMDB2P-4bPMv2DnwVNDZozCIIlHdaEMLj8hzP'
        '-QJ9Q9LQ-EW14Z6YvKDbiGx0WmYQc3jAPbw3Tb3ASXuEPg3FEA',
        skypeExpiry,
        'registrationToken=U2lnbmF0dXJlOjI6Mjg6QVFRQUFBREtUNStkdDdkaS'
        '94K0dta1NQRGR6TztWZXJzaW9uOjY6MToxO0lzc3VlVGltZTo0OjE5OjUyND'
        'g3ODk2MTIyODA0MDYzMzQ7RXAuSWRUeXBlOjc6MTo4O0VwLklkOjI6MjY6bG'
        'l2ZTouY2lkLjMwNjNlOTQ0OTU0YWU2NTk7RXAuRXBpZDo1OjM2OjViYjg1ZD'
        'YzLTk4MjMtNGFjMC05YjNhLTVmNmMyODY1NTA4NTtFcC5Mb2dpblRpbWU6Nz'
        'oxOjA7RXAuQXV0aFRpbWU6NDoxOTo1MjQ4Nzg5NjEyMjc5NjI0Nzc3O0VwLk'
        'F1dGhUeXBlOjc6MjoxNTtFcC5FeHBUaW1lOjQ6MTk6NTI0ODc5MDQxMTU0Nz'
        'M4NzkwNDtVc3IuTmV0TWFzazoxMToxOjI7VXNyLlhmckNudDo2OjE6MDtVc3'
        'IuUmRyY3RGbGc6MjowOjtVc3IuRXhwSWQ6OToxOjA7VXNyLkV4cElkTGFzdE'
        'xvZzo0OjE6MDtVc2VyLkF0aEN0eHQ6Mjo0NDg6Q2xOcmVYQmxWRzlyWlc0YW'
        'JHbDJaVG91WTJsa0xqTXdOak5sT1RRME9UVTBZV1UyTlRrQkExVnBZeFF4TH'
        'pFdk1EQXdNU0F4TWpvd01Eb3dNQ0JCVFF4T2IzUlRjR1ZqYVdacFpXUlo1a3'
        'FWUk9sak1BQUFBQUFBQUVBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBYWJHbD'
        'JaVG91WTJsa0xqTXdOak5sT1RRME9UVTBZV1UyTlRrQUFBQUFBQUFBQUFBSF'
        'RtOVRZMjl5WlFBQUFBQUVBQUFBQUFBQUFBQUFBQUJaNWtxVlJPbGpNQUFBQU'
        'FBQUFBQUFBQUFBQUFBQUFBQUFBUnBzYVhabE9pNWphV1F1TXpBMk0yVTVORF'
        'E1TlRSaFpUWTFPUUFBQUFBQUVOL2NYUWdBQUFBRFZXbGpDRWxrWlc1MGFYUj'
        'VEa2xrWlc1MGFYUjVWWEJrWVhSbENFTnZiblJoWTNSekRrTnZiblJoWTNSel'
        'ZYQmtZWFJsQ0VOdmJXMWxjbU5sRFVOdmJXMTFibWxqWVhScGIyNFZRMjl0Yl'
        'hWdWFXTmhkR2x2YmxKbFlXUlBibXg1QUFBPTs=',
        regExpiry,
        'https://azneu1-client-s.gateway.messenger.live.com/v1'
    ]
