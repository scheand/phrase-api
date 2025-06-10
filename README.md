
us-central1-docker.pkg.dev/tough-flow-460911-j0/phrase-api-repo

export GOOGLE_PROJECT_ID=tough-flow-460911-j0    

export GEMINI_API_KEY=key

## Authenticate Docker with GCP:

    gcloud auth login
    gcloud auth configure-docker

## Set your GCP project

    gcloud config set project $GOOGLE_PROJECT_ID

## Deploying to GCP service:

    docker build --platform linux/amd64 -t gcr.io/$GOOGLE_PROJECT_ID/phrase-api .
    docker build -t gcr.io/tough-flow-460911-j0/phrase-api .

## Push to Google Container Registry

    docker push gcr.io/$GOOGLE_PROJECT_ID/phrase-api

## Deploy to Cloud Run

    gcloud run deploy phrase-api \
        --image gcr.io/$GOOGLE_PROJECT_ID/phrase-api \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY

## Run Docker container Locally:

    docker run --rm -p 8080:8080 \
        -e GEMINI_API_KEY='$GEMINI_API_KEY' \
        --name phrase-api gcr.io/tough-flow-460911-j0/phrase-api:latest

## Run locally the file (without Docker)

  ```console
    uvicorn main:app --reload
  ```

# Teraform

## locally init
cd terraform
export GOOGLE_APPLICATION_CREDENTIALS=~/cloudbuild-sa-703.json
terraform init
    
