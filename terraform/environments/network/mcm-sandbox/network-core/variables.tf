variable "entity" {
  description = "Entity name"
  type        = string
}

variable "routing_domain" {
  description = "Routing domain level"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "tgw_name" {
  description = "Simulated TGW name"
  type        = string
}

variable "amazon_side_asn" {
  description = "Simulated AWS-side ASN"
  type        = number
}

variable "customer_gateways" {
  description = "Simulated VPNs. Each entry can independently use static or BGP routing."
  type = map(object({
    name               = string
    ip_address         = string
    bgp_asn            = number
    static_routes_only = optional(bool, false)
  }))
}

variable "protect_from_destroy" {
  description = "Simulates production protection. When true, Terraform blocks accidental destroy."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}
