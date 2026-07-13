# Monitoring Setup

## Install
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

## Access Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# Open http://localhost:3000
# Username: admin
# Password: kubectl get secret -n monitoring monitoring-grafana \
#   -o jsonpath="{.data.admin-password}" | base64 --decode

## Key Dashboards
- Kubernetes / Compute Resources / Pod — CPU + memory per pod
- Kubernetes / Compute Resources / Namespace — cluster overview
