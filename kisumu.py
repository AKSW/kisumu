import click
from loguru import logger
from jinja_rdf.rdf_property import (
    rdf_properties,
    rdf_inverse_properties,
    rdf_property,
    rdf_inverse_property,
)
from jinja_rdf.sparql_query import sparql_query
from rdflib import Graph, URIRef
from rdflib.util import from_n3
from rdflib.namespace import Namespace
from jinja_rdf.rdf_resource import RDFResource
import jinja2
import sys
from pathlib import Path


def jinja_template(template: str | jinja2.Template | Path, graph: Graph):
    templateLoader = None
    if isinstance(template, Path):
        templateLoader = jinja2.FileSystemLoader(searchpath="/")
    environment = jinja2.Environment(loader=templateLoader)
    environment.filters["properties"] = rdf_properties
    environment.filters["properties_inv"] = rdf_inverse_properties
    environment.filters["property"] = rdf_property
    environment.filters["property_inv"] = rdf_inverse_property
    environment.filters["query"] = sparql_query
    if isinstance(template, Path):
        return environment.get_template(str(template))
    else:
        return environment.from_string(template)


def get_context(graph: Graph, resource: RDFResource | URIRef | str):
    n = {
        prefix: Namespace(namespace)
        for prefix, namespace in graph.namespace_manager.namespaces()
    }
    namespaces = {prefix.upper(): namespace for prefix, namespace in n.items()}
    return {
        **namespaces,
        "resource": RDFResource(graph, resource, graph.namespace_manager),
        "graph": graph,
        "namespace_manager": graph.namespace_manager,
        "n": n,
    }


def render(
    template: str | jinja2.Template | Path,
    graph: Graph,
    resource: RDFResource | URIRef | str,
):
    return jinja_template(template, graph).render(get_context(graph, resource))


def stream(
    template: str | jinja2.Template | Path,
    graph: Graph,
    resource: RDFResource | URIRef | str,
):
    return jinja_template(template, graph).stream(get_context(graph, resource))


@click.group()
@click.option("--loglevel", default="INFO")
def cli(loglevel):
    logger.remove()
    logger.add(sys.stderr, level=loglevel)
    if loglevel in ["DEBUG"]:
        logger.debug(f"Loglevel is {loglevel}")


@cli.command()
@click.option("--template", "-t")
@click.option("--graph", "-g")
@click.option(
    "--resource",
    "-r",
    help="Provide the resource IRI in n3 syntax (e.g. <https://example.org/res>)",
)
@click.option("--compatibility", "-c", default=None)
@click.option("--output", "-o", default="-")
def build(template, graph, resource, output, compatibility):
    if compatibility == "jekyll-rdf":
        click.echo(
            "Currently there is no compatibility to jekyll-rdf implemented, it will probably not cover 100% but if you would like to implement some thing, please send me pull-requests."
        )
        return

    if output == "-":
        output = sys.stdout

    g = Graph()
    g.parse(graph)

    stream(
        template=Path(template).absolute(), graph=g, resource=from_n3(resource)
    ).dump(output)
