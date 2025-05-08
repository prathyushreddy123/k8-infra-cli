import os
import yaml
import click
from jsonschema import validate, ValidationError, SchemaError

def load_yaml_file(path):
    """Utility to load and parse a YAML file."""
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise click.ClickException(f"Failed to load YAML file: {path} -> {e}")

@click.command()
@click.option(
    "--config-file", "-f",
    required=True,
    type=click.Path(exists=True),
    help="Path to the cluster config YAML file"
)
@click.option(
    "--schema-file", "-s",
    required=True,
    type=click.Path(exists=True),
    help="Path to the schema YAML or JSON file"
)
def validate_config(config_file, schema_file):
    """
    Validate a cluster config file against a schema definition.
    """
    click.echo(f"📥 Validating config: {config_file}")
    config = load_yaml_file(config_file)
    schema = load_yaml_file(schema_file)

    try:
        validate(instance=config, schema=schema)
        cloud = config.get("cloud", "unknown").upper()
        click.echo(f"✅ Config is valid for {cloud}")
    except ValidationError as e:
        click.echo("❌ Config validation failed!")
        click.echo(f"🔍 Error: {e.message}")
        if e.path:
            click.echo(f"📍 Path: {' > '.join(map(str, e.path))}")
        raise click.Abort()
    except SchemaError as e:
        click.echo("❌ Schema file is not a valid JSON schema!")
        raise click.ClickException(str(e))
