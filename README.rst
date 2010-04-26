Jimmy Page alpha 0.1
====================

Jimmy Page is a simple caching app for Django, inspired by `Johnny Cache
<http://packages.python.org/johnny-cache/>`_, but for whole pages rather than
querysets.  It is an automatic generation-based page cache.  

If Johnny Cache (generational caching of querysets) is the first line of
defense, Jimmy Page is the last: it caches whole pages using a technique
similar to that described by `Open Logic
<http://assets.en.oreilly.com/1/event/27/Accelerate%20your%20Rails%20Site%20with%20Automatic%20Generation-based%20Action%20Caching%20Presentation%201.pdf>`_
from the Rails community.  Jimmy caches pages forever, using a "generation"
number as part of the cache key.  When any model is saved, the generation is
incremented, which expires the whole cache.  

This technique ensures that whenever the database is updated, no part of the
site will contain stale content.  It is a conservative approach which allows
Jimmy to function in a drop-in manner without any domain-specific knowledge of
how data updates might affect the output of views.  It will greatly speed up
slowly updated sites, especially when used in combination with Johnny Cache and
carefully designed, more aggressive caching for particularly intensive views.
This technique is not likely to be effective in sites that have a high ratio of
database writes to reads.

Installation
------------

This is the first, as yet largely untested alpha release.  Some notes:

* In order to function properly, `Johnny Cache
  <http://packages.python.org/johnny-cache/>`_ should be installed and used.
  Johnny Cache patches the Django caching framework to allow caching with
  infinite timeouts.  If you don't want to use Johnny Cache, you should set
  the ``JIMMY_PAGE_CACHE_SECONDS`` setting to something other than 0.
* If you have any custom SQL that updates the database without emitting
  ``post_save`` or ``pre_delete`` signals, things might get screwy.  At this
  stage, Jimmy Page works best with sites using vanilla ORM calls.

Install using pip::
    ``pip install -e git://github.com/yourcelf/django-jimmypage.git#egg=django-jimmypage``
or setup.py::
    ``python setup.py install``

Usage
-----

To use, include ``jimmypage`` in your INSTALLED_APPS setting, and define
``JIMMY_PAGE_CACHE_PREFIX`` in your settings.py file::

    # settings.py
    INSTALLED_APPS = (
        ...
        "jimmypage",
        ...
    )
    JIMMY_PAGE_CACHE_PREFIX = "jp_mysite"

To cache a view, use the ``cache_page`` decorator::

    from jimmypage.cache import cache_page

    @cache_page
    def myview(request):
        ...

Any update to any table will clear the cache (by incrementing the generation),
unless the tables are included in the ``JIMMY_PAGE_EXPIRATION_WHITELIST``.  The
defaults can be overridden by defining it in your settings.py.  By default it
includes::

    JIMMY_PAGE_EXPIRATION_WHITELIST = [
        "django_session",
        "django_admin_log",
        "registration_registrationprofile",
        "auth_message",
        "auth_user",
    ]

Views are cached on a per-user, per-language, per-path basis.  Anonymous users
share a cache, but authenticated users get a separate cache, ensuring that no
user will ever see another's user-specific content.  The cache is only used if:

* The request method is ``GET``
* There are no `messages
  <http://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_ stored for
  the request
* The response status is 200
* The response does not contain a ``Pragma: no-cache`` header

Please contribute any bugs or improvements to help make this better!

TODO
----

Current TODOs include:

* Much more testing, analysis, and code review
* middleware to apply the caching to everything, and a decorator to exclude
  particular views
* Hooks into Django Debug Toolbar to make debugging easier
