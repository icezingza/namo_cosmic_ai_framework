terraform {
  required_version = ">= 1.3.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_network" "infinity" {
  name                    = "infinity-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "infinity" {
  name          = "infinity-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.infinity.id
}
