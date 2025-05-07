import click
import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from utils.validation import validate_config_file

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to config YAML')
def render(config_file):
    """Render cloud-specific template using config and save to /output/."""
    try:
        # ✅ Step 1: Validate config and load it
        config = validate_config_file(config_file)

        cloud = config.get("cloud", "").lower()
        cluster_name = config.get("cluster", {}).get("name", "default-cluster")
        output_ext = "yaml" if cloud in ["aws", "gcp"] else "json"

        # Step 2: Set up Jinja2 environment
        template_dir = f"templates/{cloud}"
        env = Environment(loader=FileSystemLoader(template_dir))

        try:
            template = env.get_template(f"cluster_config.{output_ext}.j2")
        except TemplateNotFound:
            click.echo(f"❌ Template not found for cloud: {cloud}")
            return

        # Step 3: Render and save
        rendered_output = template.render(config)
        os.makedirs("output", exist_ok=True)
        output_file = f"output/{cluster_name}-cluster.{output_ext}"

        with open(output_file, "w") as out:
            out.write(rendered_output)

        click.echo(f"✅ Rendered template saved to: {output_file}")

    except Exception as e:
        click.echo(f"❌ Render failed: {e}")
