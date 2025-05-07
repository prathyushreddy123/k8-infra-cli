# 🌐 Multi-Cloud Infrastructure Provisioning CLI for Kubernetes

This CLI tool allows platform and DevOps teams to self-serve Kubernetes infrastructure across AWS, Azure, and GCP by submitting YAML-based configuration files. The CLI handles validation, templating, and infrastructure provisioning — all via simple commands.

---

## 🚀 Features

- ✅ Schema validation of infrastructure configs
- 🧱 Modular CLI with commands for load, validate, render, and apply
- 🌍 Multi-cloud support: AWS, Azure, GCP
- 🧰 Jinja2 templating for cloud-native config generation
- 🛠️ Extensible backend (eksctl, az, gcloud, Terraform-ready)
- 🧪 CI/CD-friendly `validate` command
- 🧩 Default config merging (optional)

---

## 🗂️ Project Structure

```bash
multi-cloud-infra-cli/
├── cli/                    # CLI command files
│   ├── apply_infra.py
│   ├── load_config.py
│   ├── render_templates.py
│   └── validate_config.py
├── utils/                  # Shared logic
│   └── validation.py
├── configs/
│   ├── schema/             # JSONSchema files per cloud
│   └── defaults/           # Optional default values
├── examples/               # Sample team configurations
│   ├── aws-sample.yaml
├── templates/              # Jinja templates per cloud
│   ├── aws/
│   ├── azure/
│   └── gcp/
└── output/                 # Rendered templates
```

---

## 🧪 CLI Commands

### `validate`
```bash
infra-cli validate --config-file examples/aws-sample.yaml
```
- ✅ Validates config against schema
- Useful for CI/CD or early feedback

---

### `load`
```bash
infra-cli load --config-file examples/aws-sample.yaml
```
- 🔍 Validates and prints cloud, region, version, environment
- Great for debugging and confirming inputs

---

### `render`
```bash
infra-cli render --config-file examples/aws-sample.yaml
```
- 📄 Renders cloud-native infra templates from YAML
- Outputs to `/output/` directory
- Supports AWS (eksctl), Azure, and GCP

---

### `apply`
```bash
infra-cli apply --config-file examples/aws-sample.yaml
```
- 🚀 Simulates or triggers provisioning (eksctl/gcloud/az)
- Will use Terraform in future versions

---

## 📦 Sample Config

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

## 📖 Docs

- [Phase 1: Why I’m Building This CLI](https://prathyushdommata.hashnode.dev/kubernetes-cli)
- [Phase 2: Validated Config-Driven CLI Design](https://prathyushdommata.hashnode.dev/robust-kubernetes-cli)

---

## 🧠 Roadmap

- [ ] Real provisioning using `eksctl`, `az`, `gcloud`
- [ ] Merge optional defaults from `configs/defaults/`
- [ ] GitOps-style template sync using Flux
- [ ] Terraform backend support

---

## 🙌 Contributions

We welcome PRs and ideas for improvement. Reach out if you're building a similar internal DevOps platform!

---

## 🏃‍♂️ Quick Start

```bash
# Validate
infra-cli validate --config-file examples/aws-sample.yaml

# Preview config
infra-cli load --config-file examples/aws-sample.yaml

# Render template
infra-cli render --config-file examples/aws-sample.yaml

# Apply (Coming Soon)
infra-cli apply --config-file examples/aws-sample.yaml
```

---

## 📬 License

MIT License — happy building 🚀