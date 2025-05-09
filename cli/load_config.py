import click
from infra_cli.utils.validation import validate_config_file

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to your YAML config')
def load(config_file):
    """Load and parse a cluster config YAML file."""
    try:
        # ✅ Validate and load full config using shared utility
        config = validate_config_file(config_file)

        cloud = config.get('cloud', 'unknown')
        cluster_name = config.get('cluster', {}).get('name', 'undefined')
        region = config.get('account', {}).get('region', 'undefined')
        version = config.get('cluster', {}).get('version', 'unknown')
        environment = config.get('account', {}).get('environment', 'dev')

        click.echo("✅ Config Summary:")
        click.echo(f"   ☁️  Cloud       : {cloud}")
        click.echo(f"   🔧 Cluster Name: {cluster_name}")
        click.echo(f"   🌍 Region      : {region}")
        click.echo(f"   🧪 Version     : {version}")
        click.echo(f"   🏷️  Environment : {environment}")
        click.echo(f"   ✅ Validation passed successfully")

    except Exception as e:
        click.echo(f"❌ Failed to load config: {e}")
