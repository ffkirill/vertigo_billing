# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Person


class PersonTest(TestCase):
    def setUp(self):
        self.p1 = Person.objects.create(surname="Иванов",
                                        name="Иван",
                                        last_name="Иванович")
        self.p2 = Person.objects.create(name="Иван",
                                        last_name="Иванович")
        self.p3 = Person.objects.create(surname="Иванов",
                                        name="Иван")
        self.p4 = Person.objects.create(name="Иван")
        self.p5 = Person.objects.create(surname="Иванов",
                                        last_name="Иванович")

    def test_short_name(self):
        self.assertEqual(unicode(self.p1), "Иванов И. И.")
        self.assertEqual(unicode(self.p2), "Иван")
        self.assertEqual(unicode(self.p3), "Иванов И.")
        self.assertEqual(unicode(self.p4), "Иван")
        with self.assertRaises(ValidationError):
            self.p5.full_clean()
