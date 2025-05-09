import click
import os
import subprocess
from infra_cli.utils.validation import validate_config_file

@click.command()
@click.option('--config-file', '-f', required=True, type=click.Path(exists=True), help='Path to input YAML config')
@click.option('--dry-run', is_flag=True, default=False, help='Print the provisioning command without executing it')
@click.option('--auto-approve', is_flag=True, default=False, help='Skip interactive confirmation')
def apply(config_file, dry_run, auto_approve):
    """Apply the infrastructure using native CLI tools (eksctl, az, gcloud)."""

    try:
        # ✅ Validate config
        config = validate_config_file(config_file)
        cloud = config.get("cloud", "").lower()
        cluster_name = config.get("cluster", {}).get("name", "default-cluster")
        output_file = f"output/{cluster_name}-cluster.yaml" if cloud != "azure" else f"output/{cluster_name}-cluster.json"

        if not os.path.exists(output_file):
            click.echo(f"❌ Rendered output not found: {output_file}. Please run `render` first.")
            return

        # ✅ Build the provisioning command
        if cloud == "aws":
            command = ["eksctl", "create", "cluster", "-f", output_file]
        elif cloud == "azure":
            command = [
                "az", "deployment", "group", "create",
                "--template-file", output_file,
                "--resource-group", config.get("account", {}).get("resourceGroup", "my-rg")
            ]
        elif cloud == "gcp":
            # Simplified example; normally you'd pull values from config and generate a full command
            cluster = config.get("cluster", {})
            account = config.get("account", {})
            command = [
                "gcloud", "container", "clusters", "create", cluster.get("name", "gke-cluster"),
                "--region", account.get("region", "us-central1"),
                "--num-nodes", "3"
            ]
        else:
            click.echo("❌ Unsupported cloud provider.")
            return

        click.echo(f"🧠 Provisioning command:\n{' '.join(command)}")

        if dry_run:
            click.echo("💡 Dry run mode enabled. No changes were made.")
            return

        if not auto_approve:
            click.confirm("⚠️ Do you want to proceed with provisioning?", abort=True)

        # ✅ Execute the provisioning command
        subprocess.run(command, check=True)
        click.echo("✅ Provisioning complete.")

    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Command failed: {e}")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
