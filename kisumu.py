import click
from loguru import logger
from jinja_rdf.rdf_property import rdf_property, rdf_inverse_property
from rdflib import Graph
from rdflib.util import from_n3
from jinja_rdf.rdf_resource import cast
import jinja2
from sys import stdout, stderr


@click.group()
@click.option("--loglevel", default="INFO")
def cli(loglevel):
    logger.remove()
    logger.add(stderr, level=loglevel)
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
        pass

    if output == "-":
        output = stdout.buffer

    class Page:
        rdf = None

    g = Graph()
    g.parse(graph)

    page = Page()
    page.rdf = cast(g.resource(from_n3(resource)))

    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    environment = jinja2.Environment(loader=templateLoader)
    environment.filters["property"] = rdf_property
    environment.filters["inv_property"] = rdf_inverse_property
    template = environment.get_template(template)
    template.stream(page=page).dump(output, encoding="utf-8")
