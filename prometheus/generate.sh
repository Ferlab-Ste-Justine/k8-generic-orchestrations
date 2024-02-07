#!/bin/bash

chart_version="54.1.0"
operator_version="0.69.1"
crds_required=("alertmanagerconfigs" "alertmanagers" "podmonitors" "probes" "prometheuses" "prometheusrules" "servicemonitors" "thanosrulers")

create_kustomization_file() {
  cat <<EOF >kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - namespace.yml
EOF
}

append_to_kustomization_file() {
  echo "  - $1" >> kustomization.yaml
}

create_kustomization_file

echo "Rendering Helm Template..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
if helm template prometheus prometheus-community/kube-prometheus-stack -f values.yml --version=$chart_version > prometheus.yml
then
  sed -i 's|registry.k8s.io/kube-state-metrics/kube-state-metrics|index.docker.io/ferlabcrsj/kube-state-metrics.kube-state-metrics|g' prometheus.yml
  echo "Successful render."
  append_to_kustomization_file "prometheus.yml"
else
  echo "Failed render."
  exit 1
fi

echo

echo "Downloading Kubernetes CRDs..."
for crd in "${crds_required[@]}"
do
  if wget -q "https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v$operator_version/example/prometheus-operator-crd/monitoring.coreos.com_$crd.yaml" -P crds -N
  then
    echo "Successful download of '$crd'."
    append_to_kustomization_file "crds/monitoring.coreos.com_$crd.yaml"
  else
    echo "Failed download of '$crd'."
    exit 1
  fi
done
