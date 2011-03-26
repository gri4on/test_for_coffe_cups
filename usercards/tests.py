# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from test_for_coffe_cups.usercards.models import UserCard
from test_for_coffe_cups.usercards.models import action_callback
from test_for_coffe_cups.usercards.models import ObjectsChanged
import datetime
from test_for_coffe_cups.usercards.models import MiddlewareData
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


from django.db.models.query import QuerySet
from pprint import PrettyPrinter

def dprint(object, stream=None, indent=1, width=80, depth=None):
    # Catch any singleton Django model object that might get passed in
    if getattr(object, '__metaclass__', None):
        if object.__metaclass__.__name__ == 'ModelBase':
            # Convert it to a dictionary
            object = object.__dict__

    # Catch any Django QuerySets that might get passed in
    elif isinstance(object, QuerySet):
        # Convert it to a list of dictionaries
        object = [i.__dict__ for i in object]

    # Pass everything through pprint in the typical way
    printer = PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(object)

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
        """
        Test on context processor page
        """
        client = Client()
        response = client.get("/ctx_proc/")
        settings_ctx = response.context['settings']
        self.failUnlessEqual(settings_ctx.DATABASES, settings.DATABASES)

    def testHttp_2(self):
        """
        Test on main page
        """
        client = Client()
        response = client.get("/")
        settings_ctx = response.context['settings']
        self.failUnlessEqual(settings_ctx.DATABASES, settings.DATABASES)


class SignalsTest(TestCase):

    def testSignal(self):
        """
        Test - we have in db last record with changed object
        """
        instance = UserCard.objects.latest('id')
        action_callback(sender=UserCard, created = True, instance = instance)
        ins = ObjectsChanged.objects.latest('id')
        self.failUnlessEqual(instance, ins.model_object.get_object_for_this_type())

class TestLinkToAdmin(TestCase):

    def testHttp(self):
        client = Client()
        # Authenticate to get page with admin interface
        response = client.post('/accounts/login/', {'username': 'admin', 'password': 'admin'}, follow=True)

        # Test - we authenticated ?
        self.failUnlessEqual(response.status_code, 200)

        response = client.get("/")
        print response.content

        # Check do we have link to admin
        self.assertContains(response, "/admin/usercards/usercard/1/")
