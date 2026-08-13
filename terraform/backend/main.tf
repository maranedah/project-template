# Backend Cloud Run v2 service (stub — uncomment on first deploy).
# Serverless tuning notes: docs/03-technical/04-architecture-definition/01-cloud-stack.md

# resource "google_cloud_run_v2_service" "backend" {
#   name     = "${var.prefix}-backend-${var.env}"
#   location = var.region
#
#   template {
#     containers {
#       image = var.image
#       ports { container_port = 8000 }
#       resources {
#         limits            = { cpu = "1", memory = "512Mi" }
#         cpu_idle          = true   # bill CPU only while serving requests
#         startup_cpu_boost = true   # faster cold starts
#       }
#       # Secrets come from Secret Manager references, never plaintext env
#       # (docs/03-technical/08-security/01-secrets.md):
#       # env {
#       #   name = "APP_DATABASE_URL"
#       #   value_source {
#       #     secret_key_ref { secret = "app-database-url", version = "latest" }
#       #   }
#       # }
#     }
#     scaling { max_instance_count = 4 }
#   }
# }

output "service_url" {
  value = "" # google_cloud_run_v2_service.backend.uri once enabled
}
