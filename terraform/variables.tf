variable "project_id" {
  description = "GCP project id (dev or prod project, selected by CI branch)"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "southamerica-west1"
}

variable "env" {
  description = "Environment name: dev | prod"
  type        = string
  default     = "dev"
}

variable "prefix" {
  description = "Resource name prefix"
  type        = string
  default     = "PROJECT_NAME"
}

variable "backend_image" {
  description = "Backend container image (tagged with the git sha by CI)"
  type        = string
  default     = ""
}

variable "frontend_image" {
  description = "Frontend container image (tagged with the git sha by CI)"
  type        = string
  default     = ""
}
