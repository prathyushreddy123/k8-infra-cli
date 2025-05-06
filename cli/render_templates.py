import click
import yaml
import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to config YAML')
def render(config_file):
    """Render cloud-specific template using config and save to /output/."""
    try:
        # Load config
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        cloud = config.get("cloud", "").lower()
        cluster_name = config.get("cluster", {}).get("name", "default-cluster")

        if cloud not in ["aws", "azure", "gcp"]:
            click.echo("❌ Unsupported cloud. Choose from aws, azure, or gcp.")
            return

        # Map output format
        output_ext = "yaml" if cloud in ["aws", "gcp"] else "json"

        # Set up Jinja2
        template_dir = f"templates/{cloud}"
        env = Environment(loader=FileSystemLoader(template_dir))

        try:
            template = env.get_template(f"cluster_config.{output_ext}.j2")
        except TemplateNotFound:
            click.echo(f"❌ Template not found for cloud: {cloud}")
            return

        rendered_output = template.render(config)

        # Save output
        os.makedirs("output", exist_ok=True)
        output_file = f"output/{cluster_name}-cluster.{output_ext}"
        with open(output_file, "w") as out:
            out.write(rendered_output)

        click.echo(f"✅ Rendered template saved: {output_file}")

    except Exception as e:
        click.echo(f"❌ Render error: {e}")
