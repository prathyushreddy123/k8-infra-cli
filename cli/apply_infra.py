import click

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to rendered config file')
def apply(config_file):
    """Apply the infrastructure using a provider's tool (e.g. Terraform, eksctl)."""
    click.echo(f"🚀 Applying infrastructure defined in: {config_file}")
    click.echo("🛠️ Execution logic for Terraform/eksctl/az CLI will be added in Phase 5.")
