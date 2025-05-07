import click
import yaml
import os
from jsonschema import validate, ValidationError

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to YAML config file')
def validate_config(config_file):
    """Validate the config structure using a per-cloud schema."""
    try:
        # Load user config
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        cloud = config.get("cloud", "").lower()
        if cloud not in ["aws", "azure", "gcp"]:
            click.echo("Missing or unsupported cloud provider in config file.")
            return

        # Load schema
        schema_path = os.path.join("configs", "schema", f"{cloud}-schema.yaml")
        if not os.path.exists(schema_path):
            click.echo(f"Schema not found for cloud: {cloud}")
            return

        with open(schema_path, 'r') as f:
            schema = yaml.safe_load(f)

        # Validate config
        validate(instance=config, schema=schema)
        click.echo(f"Config file is valid for {cloud.upper()}")

    except ValidationError as ve:
        click.echo(f"Schema validation error: {ve.message}")
    except Exception as e:
        click.echo(f"Error loading config: {e}")
