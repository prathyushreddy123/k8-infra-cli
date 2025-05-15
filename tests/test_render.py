import pytest
import os
from click.testing import CliRunner
from cli.render_templates import render
import yaml

@pytest.fixture
def aws_config():
    return {
        "cloud": "aws",
        "cluster": {
            "name": "test-cluster",
            "version": "1.24",
            "nodeGroups": [
                {
                    "name": "ng-1",
                    "instanceType": "t3.medium",
                    "desiredCapacity": 2
                }
            ]
        },
        "account": {
            "region": "us-west-2",
            "environment": "test"
        }
    }

@pytest.fixture
def setup_templates(tmp_path):
    # Create templates directory structure
    templates_dir = tmp_path / "templates" / "aws"
    templates_dir.mkdir(parents=True)
    
    # Create a sample template
    template_content = """
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: {{ cluster.name }}
  region: {{ account.region }}
nodeGroups:
{%- for ng in cluster.nodeGroups %}
  - name: {{ ng.name }}
    instanceType: {{ ng.instanceType }}
    desiredCapacity: {{ ng.desiredCapacity }}
{%- endfor %}
"""
    template_file = templates_dir / "cluster_config.yaml.j2"
    template_file.write_text(template_content)
    return tmp_path

def test_render_aws_template(tmp_path, aws_config, setup_templates):
    # Create config file
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(aws_config, f)
    
    # Create output directory
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(render, ["-f", str(config_file)])
        
        # Check if rendering was successful
        assert result.exit_code == 0
        assert "Rendered template saved" in result.output
        
        # Verify output file exists and contains expected content
        output_file = output_dir / "test-cluster-cluster.yaml"
        assert output_file.exists()
        content = output_file.read_text()
        assert "name: test-cluster" in content
        assert "region: us-west-2" in content
        assert "nodeGroups:" in content

def test_render_unsupported_cloud(tmp_path):
    invalid_config = {
        "cloud": "unsupported",
        "cluster": {"name": "test-cluster"}
    }
    
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(invalid_config, f)
    
    runner = CliRunner()
    result = runner.invoke(render, ["-f", str(config_file)])
    
    assert result.exit_code != 0
    assert "Unsupported cloud" in result.output 