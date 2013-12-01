# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.db import IntegrityError

import unittest
from accounting.models import Account, Movement
from clients.models import Person


class MovementTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name="Ivanov")
        self.account = Account.objects.get(person=self.person)

    def test_movement(self):
        self.assertEqual(self.account.balance, 0)
        m = Movement.objects.create(account=self.account,
                                    debit=10)
        self.assertEqual(Account.objects.get(pk=self.account.pk).balance, 10)
        m.save()
        m.save()
        self.assertEqual(Account.objects.get(pk=self.account.pk).balance, 10)
        Movement.objects.create(account=self.account,
                                credit=20)
        self.assertEqual(Account.objects.get(pk=self.account.pk).balance, -10)

    def test_disabled_account_movement_fails(self):
        self.account.disabled = True
        self.account.save()
        with self.assertRaises(IntegrityError):
            Movement.objects.create(account=self.account,
                                    debit=20)


class MovementDangerousTest(unittest.TestCase):
    def setUp(self):
        self.person = Person.objects.create(name="Ivanov")
        self.account = Account.objects.get(person=self.person)

    def test_movement(self):
        garbage = []
        self.assertEqual(self.account.balance, 0)
        m = Movement.objects.create(account=self.account,
                                    debit=10)
        garbage.append(m)
        self.assertEqual(Account.objects.get(pk=self.account.pk).balance, 10)
        m.credit = 10
        m.save()
        self.assertEqual(Account.objects.get(pk=m.pk).balance, 10)
        garbage.append(Movement.objects.create(account=self.account,
                                               credit=10))
        self.assertEqual(Account.objects.get(pk=self.account.pk).balance, 0)
        for g in garbage:
            g.delete()

    def tearDown(self):
        self.person.delete()
        self.account.delete()
