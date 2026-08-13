output "backend_url" {
  description = "Backend Cloud Run URL (empty until the module resources are enabled)"
  value       = module.backend.service_url
}

output "frontend_url" {
  description = "Frontend Cloud Run URL (empty until the module resources are enabled)"
  value       = module.frontend.service_url
}
