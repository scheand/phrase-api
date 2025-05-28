output "cloud_run_url" {
  value = google_cloud_run_service.phrase_api.status[0].url
  description = "URL of the deployed Cloud Run service"
}