#!/bin/bash

echo "Building Docker image..."
docker build -t webapp:1.0.0 .

echo "Applying Kubernetes manifests..."
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/webapp-deployment

echo "Getting service information..."
kubectl get service webapp-service

echo "To get the external IP address, run:"
echo "kubectl get service webapp-service --watch"

echo "To test the application:"
echo "curl http://<EXTERNAL-IP>/version"
