# k8s-infra-cli

> **Self-Service Kubernetes Infrastructure Provisioning via CLI and Helm Charts.**

---

## Overview
This project is a **Self-Service Kubernetes Infrastructure Provisioning Tool** built with **Python CLI + Helm**.  
It allows teams to **request Kubernetes infrastructure** (Namespace, ResourceQuotas, LimitRanges, RBAC roles) **on-demand** by simply running a CLI command — avoiding slow ticketing/manual provisioning.

Infrastructure is deployed using **Helm Charts** for speed, reusability, and easy management.

---

## ✨ Key Features
- Provision a **Namespace** automatically
- Set up **ResourceQuotas** (CPU, memory)
- Create **LimitRanges** to control pod/container usage
- Define and bind **RBAC Roles** for team access
- (Optional) Set **NodeAffinity** if GPU nodes are needed
- All infrastructure provisioned through **Helm install**
- Fast, reusable, and GitOps-friendly design

---

## 🏗️ Architecture Diagram
[Developer/Team Lead (CLI User)]
             │
             ▼
[Python CLI Tool]
 (Generates values.yaml based on user input)
             │
             ▼
[Helm Chart (Pre-built templates)]
             │
             ▼
[Helm Install/Upgrade]
 (Applies Namespace, Quota, RBAC to K8s Cluster)
             │
             ▼
[Kubernetes Cluster Resources Created]
 (Namespace ready for deployments!)


---

## 🚀 How It Works (Flow)

1. User runs a CLI command to request infrastructure.
2. CLI generates a custom `values.yaml` file based on user inputs.
3. User runs a `helm install` (or CLI automates it) using the generated values.
4. Kubernetes resources (Namespace, Quotas, RBAC) are created automatically.
5. Team is ready to deploy apps into their new Namespace!

---

## 📂 Project Structure

k8s-infra-cli/
├── chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── namespace.yaml
│       ├── resourcequota.yaml
│       ├── limitrange.yaml
│       ├── role.yaml
│       └── rolebinding.yaml
├── cli/
│   ├── create_request.py
│   ├── validate_request.py (optional)
│   └── apply_request.py (optional)
├── infra_cli.py         # CLI entry point
├── setup.py             # Packaging for pip install
├── requirements.txt     # Click, PyYAML libraries
├── README.md
└── examples/
    └── sample_values.yaml


---

## 📋 Example CLI Usage

```bash
# Step 1: Create values.yaml from CLI
infra-cli create --team finance --cpu 4 --memory 8Gi --gpu true --env dev

# Step 2: Install Helm chart with generated values
helm install finance-infra ./chart/ -f finance-values.yaml

teamName: finance
namespace: finance-dev

resources:
  cpu: 4
  memory: 8Gi
  gpu: true

limits:
  cpu: 8
  memory: 16Gi

roles:
  - name: deployment-admin
    rules:
      - apiGroups: ["apps"]
        resources: ["deployments"]
        verbs: ["create", "update", "patch", "delete", "get", "list"]

nodeAffinity:
  required: true
  key: "kubernetes.io/instance-type"
  operator: "In"
  values: ["gpu-node"]

## Future Enhancements

GitOps Mode: Push values.yaml automatically to Git repository (ArgoCD watches and applies).

AI Recommendations: Auto-suggest CPU/Memory based on application type.

Slack Integration: Notify teams when infra is ready.

Approval Workflows: Manager approval if requested quota is high.

Web UI Frontend: Build a lightweight web portal for requests.

## Prerequisites

Python 3.9+

Helm 3.0+

kubectl configured with appropriate access to the Kubernetes cluster

## Contribution

This project aims to make Kubernetes infra self-service simple and fast.
Feel free to contribute ideas, code, or feedback!

## License

MIT License