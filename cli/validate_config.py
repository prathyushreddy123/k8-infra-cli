import click
import yaml

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to YAML config file')
def validate(config_file):
    """Validate the config structure and required fields (basic validation)."""
    click.echo(f"🔍 Validating config: {config_file}")
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        required_keys = ['cloud', 'account', 'cluster']
        for key in required_keys:
            if key not in config:
                click.echo(f"❌ Missing key: {key}")
                return

        click.echo("✅ Config passed basic structure validation.")

    except Exception as e:
        click.echo(f"❌ Failed to validate config: {e}")
