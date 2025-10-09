output "network_id" {
  value       = google_compute_network.infinity.id
  description = "Identifier of the Infinity AI network"
}

output "subnetwork_id" {
  value       = google_compute_subnetwork.infinity.id
  description = "Identifier of the Infinity AI subnetwork"
}
