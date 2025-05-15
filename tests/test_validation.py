import pytest
import yaml
from click.testing import CliRunner
from cli.validate_config import validate_config
from cli.load_config import load

@pytest.fixture
def valid_config():
    return {
        "cloud": "aws",
        "cluster": {
            "name": "test-cluster",
            "version": "1.24",
        },
        "account": {
            "region": "us-west-2",
            "environment": "test"
        }
    }

@pytest.fixture
def schema_config():
    return {
        "type": "object",
        "required": ["cloud", "cluster", "account"],
        "properties": {
            "cloud": {"type": "string", "enum": ["aws", "azure", "gcp"]},
            "cluster": {
                "type": "object",
                "required": ["name", "version"],
                "properties": {
                    "name": {"type": "string"},
                    "version": {"type": "string"}
                }
            },
            "account": {
                "type": "object",
                "required": ["region", "environment"],
                "properties": {
                    "region": {"type": "string"},
                    "environment": {"type": "string"}
                }
            }
        }
    }

def test_validate_config_valid(tmp_path, valid_config, schema_config):
    # Create temporary config and schema files
    config_file = tmp_path / "config.yaml"
    schema_file = tmp_path / "schema.yaml"
    
    with open(config_file, "w") as f:
        yaml.dump(valid_config, f)
    with open(schema_file, "w") as f:
        yaml.dump(schema_config, f)
    
    runner = CliRunner()
    result = runner.invoke(validate_config, ["-f", str(config_file), "-s", str(schema_file)])
    assert result.exit_code == 0
    assert "Config is valid" in result.output

def test_validate_config_invalid_cloud(tmp_path, valid_config, schema_config):
    valid_config["cloud"] = "invalid"
    
    config_file = tmp_path / "config.yaml"
    schema_file = tmp_path / "schema.yaml"
    
    with open(config_file, "w") as f:
        yaml.dump(valid_config, f)
    with open(schema_file, "w") as f:
        yaml.dump(schema_config, f)
    
    runner = CliRunner()
    result = runner.invoke(validate_config, ["-f", str(config_file), "-s", str(schema_file)])
    assert result.exit_code != 0
    assert "Config validation failed" in result.output 