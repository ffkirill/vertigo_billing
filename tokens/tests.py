from django.test import TestCase
from .models import Token, TokenReader
from clients.models import Person
from accounting.models import Account
from cable_systems.models import CableSystem, CableSystemSession
import mock
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType


class TokenProcessTest(TestCase):
    def setUp(self):

        user = User.objects.create(username="controller_1",
                                   is_active=True)

        perm = Permission.objects.get(
            content_type=ContentType.objects.get_for_model(CableSystemSession),
            codename="add_cablesystemsession")
        user.user_permissions.add(perm)

        perm = Permission.objects.get(
            content_type=ContentType.objects.get_for_model(CableSystemSession),
            codename="change_cablesystemsession")
        user.user_permissions.add(perm)

        user.set_password("1234")

        user.save()

        person = Person.objects.create(name="John Titor")
        self.person = person

        Account.objects.filter(person=person).update(balance=500)

        cable = CableSystem.objects.create(name="First cable line",
                                           rate=200)

        TokenReader.objects.create(uid="first_line_reader_one",
                                   cable_system=cable,
                                   description="First line reader one")

        Token.objects.create(name="John Titor's token",
                             value="john_titors_token",
                             person=person)

    def test_session_start_and_stop(self):
        self.client.login(username="controller_1", password="1234")

        resp = self.client.post("/tokens/process/",
                                data={"reader": "first_line_reader_one",
                                      "token": "john_titors_token"})

        self.assertTemplateUsed(resp, "tokens/process_success.html")

        self.assertTrue(CableSystemSession.objects.filter(active=True)
            .filter(person__name="John Titor",
                    cable__name="First cable line")
            .exists())

        with mock.patch.object(timezone, "now", return_value=timezone.now() +
                               timezone.timedelta(hours=2)):

            resp = self.client.post("/tokens/process/",
                                    data={"reader": "first_line_reader_one",
                                          "token": "john_titors_token"})

        session = CableSystemSession.objects.get(
            active=False,
            person__name="John Titor",
            cable__name="First cable line")

        self.assertEqual((session.date_end - session.date_start)
            .seconds, timezone.timedelta(hours=2).seconds)

        self.assertEqual(Account.objects.get(person=self.person)
                         .balance, 100)

        self.assertTemplateUsed(resp, "tokens/process_success.html")

