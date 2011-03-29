# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from test_for_coffe_cups.usercards.models import UserCard
import datetime
from test_for_coffe_cups.usercards.models import MiddlewareData
from django.conf import settings
import os
import shlex, subprocess
import re
from django.db.models import get_models
import datetime


class UserCardTest(TestCase):
    def setUp(self):
        """
        Test main page:
        Create Test user with fake data
        """
        card = UserCard.objects.all()[0]
        card.name = "UserName"
        card.last_name = "UserLastName"
        card.email = "UserEmail@example.com"
        card.jabber = "UserJabber"
        card.skype = "UserSkype"
        card.date_birth = "1980-10-10"
        card.other_contacts = "UserOtherContacts"
        card.bio = "UserBio"
        card.save()

    def testHttp(self):
        """
        Test http response, and context
        """
        client = Client()
        response = client.get("/")
        # Test http code
        self.failUnlessEqual(response.status_code, 200)
        # Test context
        cardObj = response.context['card']
        self.failUnlessEqual(cardObj.name, "UserName")
        self.failUnlessEqual(cardObj.last_name, "UserLastName")
        self.failUnlessEqual(cardObj.email, "UserEmail@example.com")
        self.failUnlessEqual(cardObj.jabber, "UserJabber")
        self.failUnlessEqual(cardObj.skype, "UserSkype")
        self.failUnlessEqual(cardObj.date_birth, datetime.date(1980, 10, 10))
        self.failUnlessEqual(cardObj.other_contacts, "UserOtherContacts")
        self.failUnlessEqual(cardObj.bio, "UserBio")
        # Test content
        self.assertContains(response, "UserName", status_code=200)
        self.assertContains(response, "UserLastName", status_code=200)
        self.assertContains(response, "UserEmail@example.com", status_code=200)
        self.assertContains(response, "UserJabber", status_code=200)
        self.assertContains(response, "UserSkype", status_code=200)
        self.assertContains(response, datetime.date(1980, 10, 10), \
                                                         status_code=200)
        self.assertContains(response, "UserOtherContacts", status_code=200)
        self.assertContains(response, "UserBio", status_code=200)


class TestMiddleware(TestCase):
    def setUp(self):
        client = Client()
        response = client.get("/middleware/")
        self.response = response

    def testHttp(self):
        response = self.response
        # Check http code
        self.failUnlessEqual(response.status_code, 200)
        # Test context
        #  - we have just one saved request in db with method GET
        #    line: 59
        middleware = response.context['middleware_list'][0]
        self.failUnlessEqual(middleware.method, "GET")

    def testObject(self):
        # Test object in database
        middleware = MiddlewareData.objects.all()[0]
        self.failUnlessEqual(middleware.method, "GET")


class TestEditUserCard(TestCase):
    def setUp(self):
        # create UserCard model with all fields
        client = Client()
        self.client = client

        # Test authentication
        #  1. Test http redirect
        #     (if user is not authenticated - redirect to login page)
        #  2. Test http auth
        #     (post auth data and check for redirect to 'edit page')
        #  3. Edit data on page (post )
        response_auth = client.get('/edit_usercard/')

        # redirect to auth page
        self.failUnlessEqual(response_auth.status_code, 302)
        response_auth = self.client.post('/accounts/login/',\
                            {'username': 'admin', 'password': 'admin'})
        # Redirect to edit page
        self.failUnlessEqual(response_auth.status_code, 302)
        response_auth = client.get("/edit_usercard/")
        self.failUnlessEqual(response_auth.status_code, 200)

        response = client.post('/edit_usercard/',\
                                 {'name'           : 'TestName',
                                  'last_name'      : 'TestLastName',
                                  'contacts'       : 'TestContacts',
                                  'email'          : 'test@example.com',
                                  'jabber'         : 'TestJabber',
                                  'skype'          : 'TestSkype',
                                  'date_birth'     : '1917-11-7',
                                  'other_contacts' : 'TestOtherContacts',
                                  'bio'            : 'TestBio'})

        self.response = response

    def testHttp(self):

        # Test http status code
        self.failUnlessEqual(self.response.status_code, 200)
        card = UserCard.objects.all()[0]

        # Test context
        self.failUnlessEqual(card.name, "TestName")
        self.failUnlessEqual(card.last_name, "TestLastName")
        self.failUnlessEqual(card.contacts, "TestContacts")
        self.failUnlessEqual(card.email, "test@example.com")
        self.failUnlessEqual(card.jabber, "TestJabber")
        self.failUnlessEqual(card.skype, "TestSkype")
        self.failUnlessEqual(card.date_birth, datetime.date(1917, 11, 7))
        self.failUnlessEqual(card.other_contacts, "TestOtherContacts")
        self.failUnlessEqual(card.bio, "TestBio")


class TestContextProcessor(TestCase):
    def testHttp_1(self):
        """Test on context processor page"""
        client = Client()
        response = client.get("/ctx_proc/")
        settings_ctx = response.context['settings']
        self.failUnlessEqual(settings_ctx.DATABASES, settings.DATABASES)

    def testHttp_2(self):
        """Test on main page"""
        client = Client()
        response = client.get("/")
        settings_ctx = response.context['settings']
        self.failUnlessEqual(settings_ctx.DATABASES, settings.DATABASES)


class TestCustomCommand(TestCase):
    def testCommandBash(self):
        # check bash script
        #management.call_command('printallmodels')
        os.system("sh test_for_coffe_cups/printallmodels.sh")

        # Check do we have any dat files in current path ?
        files = os.listdir(".")
        for _file in files:
            if _file[-3:] == "dat":
                self.failUnlessEqual(datetime.date.strftime(datetime.date.today(), \
                                                            '%Y-%m-%d') in _file, True)


        # Deleting all dat files
        os.system("rm -Rvf *.dat")


    def testCommand(self):
        args = shlex.split("python test_for_coffe_cups/manage.py printallmodels")
        process = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        # creating list of all models
        models_list = []
        for model in get_models():
            models_list.append(model.__name__)
        # Check stdout
        data = process.stdout.readlines()
        for line in data:
            res = re.findall("Model name: \'([\w]+)\' have ([\d]+) objects", line)
            name, value = res[0]
            # Test
            self.failUnlessEqual(name in models_list, True)