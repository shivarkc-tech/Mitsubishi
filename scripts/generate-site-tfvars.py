#!/usr/bin/env python3
import argparse
import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

def hcl_string(value):
    return '"' + str(value).replace('"', '\\"') + '"'

def hcl_bool(value):
    return "true" if bool(value) else "false"

def generate_tfvars(entity: str):
    yaml_path = ROOT / "config" / "entities" / f"{entity}.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"Config file not found: {yaml_path}")

    data = yaml.safe_load(yaml_path.read_text())
    network_core = data["network_core"]
    cgs = network_core["customer_gateways"]

    out_dir = ROOT / "terraform" / "environments" / "network" / entity / "network-core"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "terraform.tfvars"

    lines = []
    lines.append(f"# network-core tfvars for {entity}")
    lines.append(f"# Generated from config/entities/{entity}.yaml")
    lines.append("# DO NOT edit manually - update YAML and re-run scripts/generate-site-tfvars.py")
    lines.append("")
    lines.append(f"entity         = {hcl_string(data['entity'])}")
    lines.append(f"routing_domain = {hcl_string(data['routing_domain'])}")
    lines.append(f"region         = {hcl_string(data['region'])}")
    lines.append("")
    lines.append(f"tgw_name        = {hcl_string(network_core['tgw_name'])}")
    lines.append(f"amazon_side_asn = {network_core['amazon_side_asn']}")
    lines.append("")
    lines.append("customer_gateways = {")
    for key, cg in cgs.items():
        lines.append(f"  {key} = {{")
        lines.append(f"    name               = {hcl_string(cg['name'])}")
        lines.append(f"    ip_address         = {hcl_string(cg['ip_address'])}")
        lines.append(f"    bgp_asn            = {cg['bgp_asn']}")
        lines.append(f"    static_routes_only = {hcl_bool(cg.get('static_routes_only', False))}")
        lines.append("  }")
        lines.append("")
    lines.append("}")
    lines.append("")
    lines.append("protect_from_destroy = true")
    lines.append("")
    lines.append("tags = {")
    for k, v in data.get("tags", {}).items():
        lines.append(f"  {k} = {hcl_string(v)}")
    lines.append("}")

    out_file.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entity", required=True, help="Entity name, e.g. mcm-sandbox")
    args = parser.parse_args()
    generate_tfvars(args.entity)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
