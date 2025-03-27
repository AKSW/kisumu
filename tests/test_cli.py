import kisumu
from click.testing import CliRunner
from kisumu import cli
import importlib.resources
import simpsons_rdf


def test_build():
    runner = CliRunner()
    with importlib.resources.path(
        simpsons_rdf, "simpsons.ttl"
    ) as graph_path, importlib.resources.path(
        kisumu, "example/foaf_name.jinja"
    ) as template_path:
        result = runner.invoke(
            cli,
            [
                "build",
                "--template",
                str(template_path),
                "--graph",
                str(graph_path),
                "--resource",
                str(simpsons_rdf.SIM.Homer.n3()),
            ],
        )
        assert result.exit_code == 0
        assert result.output == "Hello, Homer Simpson!"
