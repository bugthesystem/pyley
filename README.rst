.. image:: https://github.com/ziyasal/pyley/raw/master/pyley.png?raw=true

pyley
=====

.. image:: https://img.shields.io/pypi/v/pyley.svg
    :target: https://pypi.org/project/pyley

.. image:: https://img.shields.io/pypi/pyversions/pyley.svg
    :target: https://pypi.org/project/pyley

.. image:: https://travis-ci.org/ziyasal/pyley.svg?branch=master
    :target: https://travis-ci.org/ziyasal/pyley

.. image:: https://coveralls.io/repos/ziyasal/pyley/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/ziyasal/pyley?branch=master

`Python <https://www.python.org/>`_ client for an open-source graph database **Cayley** `<https://github.com/google/cayley>`_.

    Cayley is an open-source graph inspired by the graph database behind `Freebase <http://freebase.com/>`_ and Google's `Knowledge Graph <http://www.google.com/insidesearch/features/search/knowledge.html>`_. Its goal is to be a part of the developer's toolbox where `Linked Data <http://linkeddata.org/>`_ and graph-shaped data (semantic webs, social networks, etc) in general are concerned.

Install via pip
---------------

You can install pyley using::

    $ pip install pyley

Sample
------

**Import pyley:**

.. code-block:: python

    from pyley import CayleyClient, GraphObject

    # Create cayley client
    # this creates client with default parameters `http://localhost:64210/api/v1/query/gizmo`
    client = CayleyClient()
    
    # or  specify `url` and `version` parameters
    client = CayleyClient("http://localhost:64210", "v1")
  
    g = GraphObject()

    # Query all vertices in the graph, limit to the first 5 vertices found.
    g.Vertex().GetLimit(5)
  
    # Start with only one vertex, the literal name "Humphrey Bogart", and retrieve all of them.
    query = g.Vertex("Humphrey Bogart").All();
    response = client.Send(query)
    # response.result contains JSON data and response.r contains raw response
    print response.result 
    
    # `g` and `V` are synonyms for `graph` and `Vertex` respectively, as they are quite common.
    query = g.V("Humphrey Bogart").All()
    response = client.Send(query)
    
    # "Humphrey Bogart" is a name, but not an entity. 
    # Let's find the entities with this name in our dataset.
    # Follow links that are pointing In to our "Humphrey Bogart" node with the predicate "name".
    query = g.V("Humphrey Bogart").In("<name>").All()
    response = client.Send(query)
  
    # Notice that "name" is a generic predicate in our dataset. 
    # Starting with a movie gives a similar effect.
    query = g.V("Casablanca").In("name").All()
    response = client.Send(query)

    # Relatedly, we can ask the reverse; all ids with the name "Casablanca"
    query = g.V().Has("name", "Casablanca").All()
    response = client.Send(query)
    
    # Let's get the list of actors in the film
    query = g.V().Has("name", "Casablanca") \
                  .Out("/film/film/starring") \
                  .Out("/film/performance/actor") \
                  .Out("name") \
                  .All()

    response = client.Send(query)
  
    # But this is starting to get long. 
    # Let's use a morphism -- a pre-defined path stored in a variable -- as our linkage
    film_to_actor = g.Morphism().Out("/film/film/starring").Out("/film/performance/actor")
    query = g.V() \
            .Has("name", "Casablanca") \
            .Follow(film_to_actor) \
            .Out("name") \
            .All()
    response = client.Send(query)

    # Add data programatically to the JSON result list. Can be any JSON type.
    query = g.Emit({'name': "John Doe", 'age': 41, 'isActor': True})
    response = client.Send(query)

Bugs
----

If you encounter a bug, performance issue, or malfunction, please add an `Issues <https://github.com/ziyasal/pyley/issues>`_ with steps on how to reproduce the problem
or feel to free to open a pull request.


TODO
----

- Improve Gizmo implementation (Basic steps implemented at the moment)
- Add more tests
- Add more documentation

Open Source  Projects in Use
----------------------------

- `requests <https://github.com/kennethreitz/requests>`_ by @kennethreitz

License
-------

@ziλasal & @abdullahselek
