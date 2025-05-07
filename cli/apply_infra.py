##STILL NEEDD TO DEVELOPE

import click
import subprocess
from utils.validation import validate_config_file

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to rendered config file')
def apply(config_file):
    """Apply the infrastructure using a provider's tool (eksctl, az, gcloud, or Terraform)."""
    try:
        # ✅ Step 1: Validate input file against schema
        config = validate_config_file(config_file)

        cloud = config.get("cloud", "").lower()
        cluster_name = config.get("cluster", {}).get("name", "default-cluster")
        output_file = f"output/{cluster_name}-cluster.yaml" if cloud != "azure" else f"output/{cluster_name}-cluster.json"

        click.echo(f"✅ Validated config for cloud: {cloud}")
        click.echo(f"📄 Will apply config from: {output_file}")

        # 🚀 Step 2: Dummy apply logic — replace with real calls later
        if cloud == "aws":
            click.echo(f"💻 Running: eksctl create cluster -f {output_file}")
            # subprocess.run(["eksctl", "create", "cluster", "-f", output_file], check=True)
        elif cloud == "azure":
            click.echo(f"💻 Running: az deployment group create --template-file {output_file}")
            # subprocess.run([...])
        elif cloud == "gcp":
            click.echo(f"💻 Running: gcloud container clusters create based on {output_file}")
            # subprocess.run([...])
        else:
            click.echo("❌ Unsupported cloud provider.")

        click.echo("✅ Apply process completed (simulation).")

    except Exception as e:
        click.echo(f"❌ Apply failed: {e}")
