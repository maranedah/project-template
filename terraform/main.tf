# Root: provider + module calls. State bucket injected at init
# (docs/03-technical/05-deployment/02-terraform.md). Modules ship as stubs —
# uncomment their resources on first deploy.
terraform {
  required_version = ">= 1.6"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
  backend "gcs" {}
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "backend" {
  source     = "./backend"
  project_id = var.project_id
  region     = var.region
  env        = var.env
  prefix     = var.prefix
  image      = var.backend_image
}

module "frontend" {
  source     = "./frontend"
  project_id = var.project_id
  region     = var.region
  env        = var.env
  prefix     = var.prefix
  image      = var.frontend_image
}

# Cost-runaway guard — uncomment and set billing_account on first deploy
# (docs/03-technical/04-architecture-definition/03-observability.md).
# resource "google_billing_budget" "monthly" {
#   billing_account = "FILL-BILLING-ACCOUNT-ID"
#   display_name    = "${var.prefix}-${var.env}-budget"
#   budget_filter {
#     projects = ["projects/${var.project_id}"]
#   }
#   amount {
#     specified_amount {
#       currency_code = "USD"
#       units         = "50"
#     }
#   }
#   threshold_rules { threshold_percent = 0.8 }
#   threshold_rules { threshold_percent = 1.0 }
# }
