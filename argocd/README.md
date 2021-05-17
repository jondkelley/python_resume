### Secret (local) dependencies

Used to setup kubeseal local dependencies to generate secrets

```
apt install golang-go
GOOS=$(go env GOOS)
GOARCH=$(go env GOARCH)
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.16.0/kubeseal-$GOOS-$GOARCH
sudo install -m 755 kubeseal-$GOOS-$GOARCH /usr/local/bin/kubeseal
```

### Secret creation process

```
kubectl create secret generic secret-jonk-resume-app -n resume-app --dry-run=client --from-literal=resume-update-secret=changeme123 -o yaml |  kubeseal  --controller-name=sealed-secrets  -n resume-app --controller-namespace=kube-system  --format yaml > resume-secret.yaml
```
