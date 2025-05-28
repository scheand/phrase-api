variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "gemini_api_key" {
  description = "Gemini API Key"
  type        = string
  sensitive   = true
}