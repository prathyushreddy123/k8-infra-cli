import click
from cli.create_request import create
from cli.load_config import load
from cli.render_templates import render
from cli.apply_infra import apply
from cli.validate_config import validate_config
from utils.validation import validate_config_file

@click.group()
def cli():
    """Multi-Cloud Infra CLI – Manage and provision Kubernetes infrastructure across AWS, Azure, GCP."""
    pass

cli.add_command(create)
cli.add_command(load)
cli.add_command(render)
cli.add_command(apply)
cli.add_command(validate_config)

if __name__ == "__main__":
    cli()
