# Round 2 - Scenario 2: Blog Platform on Kubernetes

## What this project does
A Flask blog REST API deployed on AWS EKS using Helm charts, with staging and
production namespaces, Horizontal Pod Autoscaling, and a Jenkins pipeline for
full CI/CD automation. No EC2, no Ansible, no Nginx configuration needed.

## What is new compared to Scenario 1
- Kubernetes replaces EC2 + Ansible + Nginx
- Two namespaces replace two servers
- AWS LoadBalancer replaces Nginx reverse proxy
- HPA automatically scales pods based on CPU load
- helm upgrade --install replaces ansible-playbook

## Architecture
    git push → Jenkins → docker build/push → helm upgrade --install
                                                  ├── staging namespace (2-5 pods, HPA)
                                                  └── production namespace (3-10 pods, HPA)

## API Endpoints
| Method | Path           | Description                    |
|--------|----------------|-------------------------------|
| GET    | /              | Welcome message                |
| GET    | /posts         | List all blog posts            |
| GET    | /posts/<id>    | Get single post by ID          |
| POST   | /comments      | Add a comment to a post        |
| GET    | /health        | Health check                   |

## Environments
| Setting      | Staging              | Production              |
|--------------|----------------------|--------------------------|
| Namespace    | staging              | production               |
| Min replicas | 2                    | 3                        |
| Max replicas | 5                    | 10                       |
| HPA target   | 70% CPU              | 70% CPU                  |
| Service type | LoadBalancer         | LoadBalancer             |

## How to deploy

Step 1 - Create EKS cluster

    eksctl create cluster --name round2-eks --region us-east-1 \
      --node-type t3.medium --nodes 2 --managed

Step 2 - Create namespaces

    kubectl create namespace staging
    kubectl create namespace production

Step 3 - Push code to GitHub to trigger Jenkins pipeline automatically

## IMPORTANT - always delete the cluster after each session

    eksctl delete cluster --name round2-eks --region us-east-1

## Key lessons from this project
- HPA requires resource requests to be set (cpu.requests) to calculate utilization
- helm upgrade --install is idempotent - safe for CI/CD pipelines
- AWS LoadBalancer type on EKS automatically provisions a real NLB with DNS hostname
- VPC limits must be checked before creating EKS (eksctl creates its own VPC)
- CloudFormation stack termination protection blocks cleanup after failed cluster creation
