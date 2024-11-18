@click.group()
@click.option('--loglevel', default="INFO")
def cli(loglevel):
    logger.remove()
    logger.add(stderr, level=loglevel)
    if loglevel in ["DEBUG"]:
        logger.debug(f"Loglevel is {loglevel}")

@cli.command()
@click.option('--template', "-t")
@click.option('--graph', "-g")
@click.option('--resource', "-r")
@click.option('--compatibility', "-c", default=None)
@click.option('--output', "-o", default="-")
def build(template, graph, output, compatibility):
    if compatibility == "jekyll-rdf":
        pass
    class Page:
        rdf = None

    page = Page()
    page.rdf = Resource()
    click.echo('Syncing')
