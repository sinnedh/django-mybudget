# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase

from mybudget.models import Organisation, Account


class BaseTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.u1.set_password('password1')
        self.u1.save()
        self.u2 = User.objects.create(username='user2')
        self.u2.set_password('password2')
        self.u2.save()
        self.u3 = User.objects.create(username='user3')
        self.u3.set_password('password3')
        self.u3.save()
        self.u4 = User.objects.create(username='user4')
        self.u4.set_password('password4')
        self.u4.save()

        self.o1 = Organisation.objects.create(name='Organisation 1')
        self.o2 = Organisation.objects.create(name='Organisation 2')

        self.a1 = Account.objects.create(organisation=self.o1, user=self.u1)
        self.a2 = Account.objects.create(organisation=self.o1, user=self.u2)
        self.a3 = Account.objects.create(organisation=self.o2, user=self.u3)
        self.a4 = Account.objects.create(organisation=self.o2, user=self.u4)

    def tearDown(self):
        pass
