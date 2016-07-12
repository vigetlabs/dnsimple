DNSimple
========

Manage your domains and associated DNS records using the DNSimple API.

Installation
------------

The simplest way to install is via pip:

.. code-block:: bash

  $ pip install dnsimple

To install a bleeding-edge version you can install from the repository:

.. code-block:: bash

  $ pip install https://github.com/vigetlabs/dnsimple/archive/master.zip

Usage
-----

The ``dnsimple.Client`` class is the entry point for managing your domains.

Authentication
~~~~~~~~~~~~~~

You can authenticate with your login and password:

.. code-block:: python

  import dnsimple
  client = dnsimple.Client(email = 'user@host.com', password = 'password')

Or with a user token:

.. code-block:: python

  import dnsimple
  client = dnsimple.Client(email = 'user@host.com', user_token = 'toke')

If you're just testing functionality, you can register a `sandbox account`_ and connect to that instead of the production API endpoint:

.. code-block:: python

  import dnsimple
  client = dnsimple.Client(email = 'user@host.com', user_token = 'toke', sandbox = True)

Managing Domains
~~~~~~~~~~~~~~~~

Once your authentication credentials are set, you can fetch a list of domains:

.. code-block:: python

  for domain in client.domains():
    print domain.id
    print domain.name
    print

Or find an individual domain:

.. code-block:: python

  domain = client.domain('foo.com') # find by domain name
  domain = client.domain(1)         # find by ID

If you want to register a domain, that is possible as well:

.. code-block:: python

  new_domain = client.domains().add({'name':'bar.com'})
  if new_domain:
    print new_domain.id
    print new_domain.name

Managing DNS Records
~~~~~~~~~~~~~~~~~~~~

Once you have found a domain whose records you want to manage, you can get a list of associated entries:

.. code-block:: python

  domain = client.domain('foo.com')
  for record in domain.records():
    print ' * {0}: "{1}" / "{2}" ({3})'.format(
      record.record_type,
      record.name,
      record.content,
      record.id
    )

Or get an individual matching record:

.. code-block:: python

  client.domain('foo.com').record('www') # find by record name
  client.domain('foo.com').record(1)     # find by ID

You can also create a new record:

.. code-block:: python

  new_record = domain.records().add({'name':'', 'record_type':'A', 'content':'192.168.1.1'})
  if new_record:
    print new_record.id
    print new_record.name
    print new_record.record_type

And destroy it when you're finished:

.. code-block:: python

  new_record.delete()

License
-------

Licensed under the `MIT License`_.

.. _sandbox account: https://developer.dnsimple.com/sandbox/
.. _MIT License: https://opensource.org/licenses/MIT
