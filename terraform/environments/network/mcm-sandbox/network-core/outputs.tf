output "simulated_vpn_parameter_names" {
  description = "SSM parameter names keyed by simulated VPN"
  value       = module.vpn_simulation.parameter_names
}

output "simulated_vpn_routing_modes" {
  description = "Current simulated routing modes from Terraform state"
  value       = module.vpn_simulation.routing_modes
}
