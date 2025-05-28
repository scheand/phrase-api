provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"
}

resource "google_project_service" "artifactregistry_api" {
  service = "artifactregistry.googleapis.com"
}

resource "google_project_service" "storage_api" {
  service = "storage.googleapis.com"
}

# Artifact Registry repository for Docker images
resource "google_artifact_registry_repository" "phrase_api_repo" {
  location      = var.region
  repository_id = "phrase-api-repo"
  format        = "DOCKER"
}

# Cloud Run service
resource "google_cloud_run_service" "phrase_api" {
  name     = "phrase-api"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/phrase-api-repo/phrase-api:latest"
        env {
          name  = "GEMINI_API_KEY"
          value = var.gemini_api_key
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.run_api, google_artifact_registry_repository.phrase_api_repo]
}

# Allow unauthenticated access (for simplicity; adjust for production)
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.phrase_api.name
  location = google_cloud_run_service.phrase_api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}