import yaml
import os
from jsonschema import validate, ValidationError

def validate_config_file(config_path: str) -> dict:
    """
    Validates the given YAML config file against its corresponding cloud schema.
    Returns the loaded and validated config dict.
    Raises an exception on validation failure.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    # Load user config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    cloud = config.get("cloud", "").lower()
    if cloud not in ["aws", "azure", "gcp"]:
        raise ValueError("Missing or unsupported 'cloud' in config. Must be one of: aws, azure, gcp.")

    # Locate schema for the cloud provider
    schema_path = os.path.join("configs", "schema", f"{cloud}-schema.yaml")
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    # Load schema
    with open(schema_path, 'r') as f:
        schema = yaml.safe_load(f)

    # Validate config against schema
    try:
        validate(instance=config, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Validation error in {config_path}: {e.message}")

    return config
