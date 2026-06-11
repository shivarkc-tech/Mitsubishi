# Mixed VPN Routing Terraform Drift Lab

This lab simulates your production scenario without creating Site-to-Site VPNs.

Production mapping:

| Real production | Lab resource |
|---|---|
| 3 Site-to-Site VPN connections | 3 SSM Parameter Store parameters |
| vpn1 live static VPN | `/terraform-drift-lab/mcm/vpn1` |
| vpn2 BGP VPN | `/terraform-drift-lab/mcm/vpn2` |
| vpn3 BGP VPN | `/terraform-drift-lab/mcm/vpn3` |
| `static_routes_only = true` | SSM value = `static` |
| `static_routes_only = false` | SSM value = `bgp` |

## Folder structure

```text
config/entities/mcm-sandbox.yaml
scripts/generate-site-tfvars.py
terraform/modules/vpn-simulation/
terraform/environments/network/mcm-sandbox/network-core/
```

## Step 1 - Generate tfvars from YAML

```bash
python3 scripts/generate-site-tfvars.py --entity mcm-sandbox
```

## Step 2 - Deploy

```bash
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core init
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core plan -out=tfplan
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core apply
```

## Step 3 - Manually modify one resource in Console

Go to:

```text
AWS Console
→ Systems Manager
→ Parameter Store
→ /terraform-drift-lab/mcm-sandbox/vpn2
→ Edit
→ Change value from static to bgp
→ Save
```

## Step 4 - Detect drift

```bash
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core plan -refresh-only -out=refresh.tfplan
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core show refresh.tfplan

terraform -chdir=terraform/environments/network/mcm-sandbox/network-core plan -out=tfplan
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core show tfplan
```

At this point Terraform should try to revert `vpn2` from `bgp` back to `static`, because YAML still says `static_routes_only: true`.

## Step 5 - Reconcile YAML

Edit:

```text
config/entities/mcm-sandbox.yaml
```

Change:

```yaml
vpn2:
  static_routes_only: false
```

Then regenerate:

```bash
python3 scripts/generate-site-tfvars.py --entity mcm-sandbox
```

Run plan again:

```bash
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core plan -out=tfplan
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core show tfplan
```

Expected result:

```text
No changes. Your infrastructure matches the configuration.
```

## Step 6 - Simulate final state

Update YAML:

```yaml
vpn1:
  static_routes_only: true
vpn2:
  static_routes_only: false
vpn3:
  static_routes_only: false
```

Regenerate and plan:

```bash
python3 scripts/generate-site-tfvars.py --entity mcm-sandbox
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core plan -out=tfplan
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core show tfplan
```

Expected: Terraform updates only `vpn3`.

## Cleanup

The module has `prevent_destroy = true` to simulate production protection. For cleanup, set this variable in `terraform.tfvars`:

```hcl
protect_from_destroy = false
```

Then:

```bash
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core plan
terraform -chdir=terraform/environments/network/mcm-sandbox/network-core destroy
```
