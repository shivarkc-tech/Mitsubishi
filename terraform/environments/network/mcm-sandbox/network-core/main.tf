locals {
  common_tags = var.tags
}

module "vpn_simulation" {
  source = "../../../../modules/vpn-simulation"

  entity               = var.entity
  routing_domain       = var.routing_domain
  tgw_name             = var.tgw_name
  amazon_side_asn      = var.amazon_side_asn
  customer_gateways    = var.customer_gateways
  protect_from_destroy = var.protect_from_destroy

  tags = local.common_tags
}
