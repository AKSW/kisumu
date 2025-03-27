import kisumu
from kisumu import render, stream
import importlib.resources
from simpsons_rdf import simpsons, SIM
from io import StringIO


def test_graph():
    from rdflib.resource import Resource

    print(simpsons)
    print(SIM.Homer)
    Resource(simpsons, SIM.Homer)


def test_render():
    template = importlib.resources.read_text(kisumu, "example/foaf_name.jinja")
    output = render(template=template, graph=simpsons.graph, resource=SIM.Homer)
    assert output == "Hello, Homer Simpson!"


def test_stream():
    with StringIO() as output:
        template = importlib.resources.read_text(kisumu, "example/foaf_name.jinja")
        stream(template=template, graph=simpsons.graph, resource=SIM.Homer).dump(output)
        assert output.getvalue() == "Hello, Homer Simpson!"

def test_query():
    template = importlib.resources.read_text(kisumu, "example/query_family.jinja")
    output = render(template=template, graph=simpsons.graph, resource=SIM.Homer)
    assert output == "Hello, Homer Simpson!"
