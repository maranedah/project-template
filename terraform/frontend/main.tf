# Frontend Cloud Run v2 service (stub — uncomment on first deploy). The nginx image
# proxies /api to the backend; point APP_BACKEND_URL at the backend service URL, or
# front both with a load balancer + CDN for custom domains.

# resource "google_cloud_run_v2_service" "frontend" {
#   name     = "${var.prefix}-frontend-${var.env}"
#   location = var.region
#
#   template {
#     containers {
#       image = var.image
#       ports { container_port = 80 }
#       resources {
#         limits            = { cpu = "1", memory = "256Mi" }
#         cpu_idle          = true
#         startup_cpu_boost = true
#       }
#     }
#     scaling { max_instance_count = 4 }
#   }
# }
#
# # Public entrypoint — users enter here only
# # (docs/03-technical/04-architecture-definition/02-connections.md).
# resource "google_cloud_run_v2_service_iam_member" "public" {
#   name     = google_cloud_run_v2_service.frontend.name
#   location = var.region
#   role     = "roles/run.invoker"
#   member   = "allUsers"
# }

output "service_url" {
  value = "" # google_cloud_run_v2_service.frontend.uri once enabled
}
