import click
import os
import subprocess
from utils.validation import validate_config_file

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to input YAML config')
@click.option('--dry-run', is_flag=True, default=False, help='Show the delete command without executing')
@click.option('--auto-approve', is_flag=True, default=False, help='Skip confirmation prompt')
def delete(config_file, dry_run, auto_approve):
    """Delete infrastructure using native CLI tools based on rendered config."""

    try:
        # Step 1: Validate and load config
        config = validate_config_file(config_file)
        cloud = config.get("cloud", "").lower()
        cluster = config.get("cluster", {})
        account = config.get("account", {})
        cluster_name = cluster.get("name", "default-cluster")

        # Step 2: Build the delete command
        if cloud == "aws":
            output_file = f"output/{cluster_name}-cluster.yaml"
            if not os.path.exists(output_file):
                raise FileNotFoundError(f"Rendered file not found: {output_file}. Please run render first.")
            command = ["eksctl", "delete", "cluster", "-f", output_file]

        elif cloud == "azure":
            resource_group = account.get("resourceGroup")
            if not resource_group:
                raise ValueError("Missing 'resourceGroup' in config for Azure.")
            command = ["az", "aks", "delete", "--name", cluster_name, "--resource-group", resource_group, "--yes"]

        elif cloud == "gcp":
            region = account.get("region", "us-central1")
            command = [
                "gcloud", "container", "clusters", "delete", cluster_name,
                "--region", region, "--quiet"
            ]
        else:
            raise ValueError("Unsupported cloud provider.")

        click.echo(f"🧨 Delete command:\n{' '.join(command)}")

        # Step 3: Dry-run mode
        if dry_run:
            click.echo("💡 Dry run mode enabled. No changes made.")
            return

        # Step 4: Confirm deletion
        if not auto_approve:
            click.confirm(f"⚠️ Are you sure you want to delete cluster '{cluster_name}'?", abort=True)

        # Step 5: Execute
        subprocess.run(command, check=True)
        click.echo(f"✅ Cluster '{cluster_name}' deleted successfully.")

    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Delete failed: {e}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
