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

The client can also pull your credentials from a ``.dnsimple`` configuration file located either in the current working directory or your home directory, though this is configurable via the ``credentials_search_paths`` option -- see ``help(dnsimple.Client)`` for details.  The format of the file is::

  [DNSimple]
  email: user@host.com
  user_token: token

This example shows token-based authentication, but any of the credentials options supported by ``dnsimple.Client`` are valid.  You can then create a client instance and the credentials will be fetched from the first credentials file found:

.. code-block:: python

  client = dnsimple.Client()

If you're just testing functionality, you can register a `sandbox account`_ and connect to that instead of the production API endpoint:

.. code-block:: python

  import dnsimple
  client = dnsimple.Client(email = 'user@host.com', user_token = 'toke', sandbox = True)

Don't forget that you'll need specify the sandbox account when authenticating via your ``.dnsimple`` configuration file:

.. code-block:: python

  client = dnsimple.Client(sandbox = True)

Managing Contacts
~~~~~~~~~~~~~~~~~

You can have multiple contacts associated with your account:

.. code-block:: python

  for contact in client.contacts():
    print contact.id
    print contact.email_address
    print

In addition to listing all contacts, you can find an individual contact by its email address:

.. code-block:: python

  contact = client.contact('user@host.com')

Or ID:

.. code-block:: python

  contact = client.contact(1)

Once you have a specific contact, you can update its attributes:

.. code-block:: python

  success = contact.update({'label': 'Technical Contact', 'email': 'new@host.com'})

You can also remove an existing contact:

.. code-block:: python

  success = contact.delete()

Registering Domains
~~~~~~~~~~~~~~~~~~~~

A contact is required when registering a new domain.  First check the status:

.. code-block:: python

  status = client.find('foo.com')

And then register the domain if it's available:

.. code-block:: python

  if status.available and status.price < 20:
    domain = client.register('foo.com', contact)

If you just want to check if the domain is available for registration (and don't need a ``Status`` object), you can do that quickly:

.. code-block:: python

  if client.check('foo.com'):
    client.register('foo.com', contact)

Managing Domains
~~~~~~~~~~~~~~~~

Whether or not your domain is registered through DNSimple, you can still manage it through the service.  You can list the domains you have already created:

.. code-block:: python

  for domain in client.domains():
    print domain.id
    print domain.name
    print

Or find an individual domain:

.. code-block:: python

  domain = client.domain('foo.com') # find by domain name
  domain = client.domain(1)         # find by ID

If you want to create a new domain, that is possible as well:

.. code-block:: python

  new_domain = client.domains().add({'name':'bar.com'})
  if new_domain:
    print new_domain.id
    print new_domain.name

And delete it if you no longer want it managed with DNSimple:

.. code-block:: python

  success = new_domain.delete()

Transferring Domains
~~~~~~~~~~~~~~~~~~~~

If you have a domain outside of DNSimple that you want to transfer in, you may do that as well:

.. code-block:: python

  success = client.transfer('foo.com', client.contact('user@host.com'))

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

You can further filter records by type:

.. code-block:: python

  for nameserver in domain.records(type = 'NS'):
      print ' * "{0}" ({1})'.format(nameserver.content, nameserver.id)

Or name:

.. code-block:: python

  for blank in domain.records(name = ''):
      print ' * {0}: "{1}" ({2})'.format(blank.record_type, blank.content, blank.id)

Or both type and name:

.. code-block:: python

  for a in domain.records(name = '', type = 'A'):
      print ' * {0}: "{1}" ({2})'.format(a.record_type, a.content, a.id)

If you want to fetch a single record, you can grab it via name or ID:

.. code-block:: python

  client.domain('foo.com').record('www') # find by record name
  client.domain('foo.com').record(1)     # find by ID

And further filter by type if necessary:

.. code-block:: python

  root = domain.record('', type = 'A')
  print ' * {0}: "{1}" ({2})'.format(root.record_type, root.content, root.id)

If the query results in an ambiguous match, an exception will be raised:

.. code-block:: python

  domain.record('', type = 'NS')
  >> dnsimple.record_collection.MultipleResultsException: Multiple results returned for query

You can also create a new record:

.. code-block:: python

  new_record = domain.records().add({'name':'', 'record_type':'A', 'content':'192.168.1.1'})
  if new_record:
    print new_record.id
    print new_record.name
    print new_record.record_type

Update an existing record:

.. code-block:: python

  success = new_record.update({'ttl': 500})

And destroy it when you're finished:

.. code-block:: python

  success = new_record.delete()

License
-------

Licensed under the `MIT License`_.

.. _sandbox account: https://developer.dnsimple.com/sandbox/
.. _MIT License: https://opensource.org/licenses/MIT
