import unittest

from django.contrib.auth.models import User, AnonymousUser
from django.contrib import messages
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from jimmypage.cache import request_is_cacheable, response_is_cacheable, get_cache_key

class Model(models.Model):
    char = models.CharField(max_length=255, blank=True, null=True)

class CacheabilityTest(unittest.TestCase):
    def test_cacheable(self):
        req = HttpRequest()
        req.path = "/some/path"
        req.method = "GET"
        self.assertTrue(request_is_cacheable(req))

        req.user = AnonymousUser()
        self.assertTrue(request_is_cacheable(req))

        req.method = "POST"
        self.assertFalse(request_is_cacheable(req))

        req.method = "GET"
        self.assertTrue(request_is_cacheable(req))

        # TODO: ensure that messages works

        res = HttpResponse("fun times")
        self.assertTrue(response_is_cacheable(res))

        redirect = HttpResponseRedirect("someurl")
        self.assertFalse(response_is_cacheable(redirect))

        res['Pragma'] = "no-cache"
        self.assertFalse(response_is_cacheable(res))

    def test_key_uniqueness(self):
        req = HttpRequest()
        req.path = "/some/path"
        req.method = "GET"
        req.user = AnonymousUser()

        req2 = HttpRequest()
        req2.path = "/some/path"
        req2.method = "GET"
        req2.user = User.objects.create(username="a_user")

        req3 = HttpRequest()
        req3.path = "/some/other/path"
        req3.method = "GET"
        req3.user = AnonymousUser()

        self.assertNotEqual(get_cache_key(req), get_cache_key(req2))
        self.assertNotEqual(get_cache_key(req), get_cache_key(req3))
