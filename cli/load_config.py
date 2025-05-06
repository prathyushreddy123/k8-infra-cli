import click
import yaml
import os

@click.command()
@click.option(
    "--config-file", "-f",
    required=True,
    type=click.Path(exists=True),
    help="Path to your multi-cloud cluster config YAML file"
)
def load(config_file):
    """
    Load a cluster config YAML file and prepare it for template rendering.
    """
    click.echo(f"Loading config from: {config_file}")

    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            cloud = config.get("cloud", "undefined").lower()

            if cloud not in ["aws", "azure", "gcp"]:
                click.echo("ERROR: Unsupported or missing cloud type. Use aws/azure/gcp.")
                return

            account = config.get("account", {})
            cluster = config.get("cluster", {})

            click.echo(f"Cloud: {cloud}")
            click.echo(f"Cluster: {cluster.get('name')} in {account.get('region')}")

            # future step: pass to Jinja2 templating engine
            click.echo("Config loaded successfully. Ready for rendering phase.")

    except Exception as e:
        click.echo(f"Failed to parse YAML file: {e}")
