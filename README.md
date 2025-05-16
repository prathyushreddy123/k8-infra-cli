# 🌐 Multi-Cloud Infrastructure Provisioning CLI for Kubernetes

This CLI tool allows platform and DevOps teams to self-serve Kubernetes infrastructure across AWS, Azure, and GCP by submitting YAML-based configuration files. The CLI handles validation, templating, and infrastructure provisioning — all via simple commands.

---

## 📋 Prerequisites

- Python 3.8 or higher
- PowerShell (Windows) or Bash (Linux/macOS)
- Cloud Provider CLI tools:
  - AWS: `eksctl` and AWS CLI v2
  - Azure: Azure CLI (`az`)
  - GCP: Google Cloud SDK (`gcloud`)
- Valid cloud provider credentials configured
- Git installed

---

## ⚙️ Installation & Setup

### Clone the Repository

You can clone the repository using either HTTPS (recommended for beginners) or SSH:

```bash
# Using HTTPS (Recommended)
git clone https://github.com/shravandeshpande1508/infra-cli.git

# Using SSH (If you have SSH keys configured)
git clone git@github.com:shravandeshpande1508/infra-cli.git
```

### Windows (PowerShell)

```powershell
# Navigate to the project directory
cd infra-cli

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Run the setup script
.\setup.ps1
```

### Linux/macOS

```bash
# Navigate to the project directory
cd infra-cli

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install cloud provider CLIs
# AWS
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Azure
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# GCP
# Follow instructions at https://cloud.google.com/sdk/docs/install
```

### Troubleshooting

#### Git Clone Issues

If you encounter SSH-related errors when cloning:

1. **Use HTTPS Instead (Quickest Solution)**
   ```bash
   git clone https://github.com/shravandeshpande1508/infra-cli.git
   ```

2. **Set Up SSH Keys (For SSH Access)**
   ```bash
   # Generate SSH key
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Start SSH agent
   eval "$(ssh-agent -s)"  # Linux/macOS
   # or
   start-ssh-agent        # Windows
   
   # Add your SSH key
   ssh-add ~/.ssh/id_ed25519
   
   # Copy the public key and add it to your GitHub account
   # Linux/macOS:
   cat ~/.ssh/id_ed25519.pub
   # Windows:
   type %USERPROFILE%\.ssh\id_ed25519.pub
   ```
   Then add the key to GitHub:
   1. Go to GitHub → Settings → SSH and GPG keys
   2. Click "New SSH key"
   3. Paste your public key and save

---

## 🚀 Features

- ✅ Schema validation of infrastructure configs
- 🧱 Modular CLI with commands for load, validate, render, and apply
- 🌍 Multi-cloud support: AWS, Azure, GCP
- 🧰 Jinja2 templating for cloud-native config generation
- 🛠️ Native cloud provider CLI integration (eksctl, az, gcloud)
- 🧪 CI/CD-friendly `validate` command
- 🔄 Dry-run support for safe testing
- 🧩 Default config merging (optional)

---

## 🗂️ Project Structure

```bash
infra-cli/
├── cli/                    # CLI command implementations
│   ├── main.py            # Main CLI entry point
│   ├── apply_infra.py     # Infrastructure provisioning
│   ├── load_config.py     # Config loading and validation
│   ├── render_templates.py # Template rendering
│   └── validate_config.py # Schema validation
├── utils/                  # Shared utilities
├── config/                 # Configuration files
│   ├── schema/            # JSONSchema files per cloud
│   └── defaults/          # Default configurations
├── templates/             # Cloud-specific Jinja templates
│   ├── aws/
│   ├── azure/
│   └── gcp/
├── tests/                 # Test suite
│   ├── test_validation.py
│   ├── test_render.py
│   └── test_apply.py
└── output/               # Generated configuration files
```

---

## 🧪 CLI Commands

### `validate-config`
```bash
infra-cli validate-config --config-file path/to/config.yaml --schema-file path/to/schema.yaml
```
- ✅ Validates configuration against cloud-specific schema
- Returns detailed validation errors if any
- Useful for CI/CD pipelines

### `load`
```bash
infra-cli load --config-file path/to/config.yaml
```
- 🔍 Loads and validates configuration
- Displays cluster details (cloud, region, version, environment)
- Helpful for configuration verification

### `render`
```bash
infra-cli render --config-file path/to/config.yaml
```
- 📄 Generates cloud-specific infrastructure templates
- Creates provider-specific output in `/output` directory
- Supports all major cloud providers

### `apply`
```bash
infra-cli apply --config-file path/to/config.yaml [--dry-run] [--auto-approve]
```
- 🚀 Provisions infrastructure using native cloud CLIs
- `--dry-run`: Preview changes without applying
- `--auto-approve`: Skip confirmation prompts

### `delete` (Coming Soon)
```bash
infra-cli delete --config-file path/to/config.yaml [--dry-run] [--auto-approve]
```
- 🗑️ Removes provisioned infrastructure
- Includes safety confirmations
- Supports dry-run mode

---

## 📦 Configuration Example

```yaml
cloud: aws
account:
  id: "123456789"
  region: "us-east-1"
  environment: "dev"
cluster:
  name: "analytics-dev"
  version: "1.29"
  chartVersion: "1.0"
nodeGroups:
  - name: apps
    instanceType: t3.medium
    min: 2
    max: 5
    desired: 3
addons:
  ingressNginx:
    enabled: true
  prometheus:
    enabled: true
identityProvider:
  enabled: true
```

---

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_validation.py

# Run with verbose output
pytest -v
```

### Test Coverage
- ✅ Configuration validation
- ✅ Template rendering
- ✅ Infrastructure provisioning
- ✅ Cloud provider integration

### Manual Testing Steps
1. Start with configuration validation
2. Test template rendering
3. Use dry-run mode for apply commands
4. Test with actual cloud provider credentials

---

## 🔐 Cloud Provider Setup

### AWS
1. Install AWS CLI v2 and eksctl
2. Configure AWS credentials (`aws configure`)
3. Ensure proper IAM permissions for EKS

### Azure
1. Install Azure CLI
2. Login to Azure (`az login`)
3. Set subscription (`az account set --subscription <id>`)

### GCP
1. Install Google Cloud SDK
2. Initialize SDK (`gcloud init`)
3. Set project and region

---

## 🛠️ Development

### Adding New Features
1. Create feature branch
2. Add tests in `tests/`
3. Implement feature
4. Update documentation
5. Submit PR

### Debug Mode
```bash
# Enable debug logging
export DEBUG=1  # Linux/macOS
$env:DEBUG=1    # Windows
```

---

## 🧠 Roadmap

- [x] Basic CLI structure and commands
- [x] AWS (eksctl) integration
- [x] Azure AKS full integration
- [ ] GCP GKE integration
- [ ] Terraform backend support
- [ ] GitOps integration with Flux
- [ ] Interactive cluster configuration
- [ ] Multi-cluster management

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more details.

---

## 📬 License

MIT License — happy building! 🚀
MIT License — happy building 🚀