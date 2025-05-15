import pytest
from click.testing import CliRunner
from cli.apply_infra import apply
import yaml
import os
from unittest.mock import patch, Mock

@pytest.fixture
def aws_config():
    return {
        "cloud": "aws",
        "cluster": {
            "name": "test-cluster",
            "version": "1.24"
        },
        "account": {
            "region": "us-west-2",
            "environment": "test"
        }
    }

@pytest.fixture
def setup_output_file(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    cluster_config = """
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: test-cluster
  region: us-west-2
"""
    output_file = output_dir / "test-cluster-cluster.yaml"
    output_file.write_text(cluster_config)
    return tmp_path

@patch("subprocess.run")
def test_apply_aws_cluster(mock_run, tmp_path, aws_config, setup_output_file):
    # Setup mock
    mock_run.return_value = Mock(returncode=0)
    
    # Create config file
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(aws_config, f)
    
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(apply, [
            "-f", str(config_file),
            "--auto-approve"  # Skip confirmation
        ])
        
        assert result.exit_code == 0
        assert "Provisioning complete" in result.output
        
        # Verify correct command was executed
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "eksctl"
        assert args[1] == "create"
        assert args[2] == "cluster"

@patch("subprocess.run")
def test_apply_dry_run(mock_run, tmp_path, aws_config, setup_output_file):
    # Create config file
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(aws_config, f)
    
    runner = CliRunner()
    result = runner.invoke(apply, [
        "-f", str(config_file),
        "--dry-run"
    ])
    
    assert result.exit_code == 0
    assert "Dry run mode enabled" in result.output
    mock_run.assert_not_called()

@patch("subprocess.run")
def test_apply_missing_output_file(mock_run, tmp_path, aws_config):
    # Create config file without creating output file
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(aws_config, f)
    
    runner = CliRunner()
    result = runner.invoke(apply, [
        "-f", str(config_file),
        "--auto-approve"
    ])
    
    assert result.exit_code != 0
    assert "Rendered output not found" in result.output
    mock_run.assert_not_called() 