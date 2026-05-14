# Example Kubernetes stack (local: minikube / kind / Docker Desktop Kubernetes)

Build and load the image into your cluster before applying:

```bash
docker build -t ecommerce-django:local .
kind load docker-image ecommerce-django:local   # if using kind
# minikube: eval $(minikube docker-env) && docker build -t ecommerce-django:local .
kubectl apply -f k8s/example-stack.yaml
kubectl port-forward svc/ecommerce-web 8080:80
```

Open `http://127.0.0.1:8080`. This is a **minimal demo** (emptyDir database, no TLS, default passwords). Replace with managed Postgres and secrets for anything beyond local practice.
