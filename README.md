# EU Ship Emissions API :ship:

This repository contains the code for an API that serves data from the [THETIS-MRV dataset](https://mrv.emsa.europa.eu/#public/emission-report) which contains emissions data for ships larger than 5,000 tons that dock in the EU.

## Setup Requirements :gear:

At the moment, the project's data files were manually downloaded from the website and saved into a GCP Cloud Storage Bucket, which were made public. However, if new data was to be added, the same manual step would have to be repeated. See the **Next steps** section below for some potential next steps to improve this process.

## Execution :computer:
The API is built using the FastAPI Python library. The data is stored in a PostgreSQL database. Both services are run using Docker containers and coordinated through Docker Compose.

To start the services, run the following command:

```
docker compose up -d 
```

This will build the Docker files and start the two services. You can verify the correct startup through the `docker compose ps` command and by opening a browser and going to `localhost:8000/docs`, which will show the Swagger docs for the API.

Upon first startup, the backend database is empty. To load the data into it, run the `load_data` endpoint in this API. It will load the files covering from 2018 to 2021. It takes several minutes to complete the action.

Once this is complete, you can run the different endpoints that are shown in the SwaggerUI documentation.

## Deployment :rocket:

This version of the code is deployed to GCP:  
- The raw data Excel files are stored in a public Storage Bucket
- Docker image hosted in a Container Registry
- The API is running on a Cloud Run service
- The database is running on a micro virtual machine
  
To access the deployed version, go to this URL:

```
https://api-se4dsyclaq-nw.a.run.app/docs
```

This page will show the SwaggerUI docs for the API, where the user can test run the different endpoints. **The data is already loaded into the deployed version and thus the `load_data` endpoint does not need to be run.**

A helper file has been added to deploy your own version of the image to a container registry. This file is `build_and_push_docker.sh`, which has a single argument, which is the version of the image being pushed.

When deploying a version to Cloud Run, you need to make sure to set the same environmental variables that are set for the API service in the `docker-compose.yml` file, this includes connection credentials for the database and the name of the GCP Bucket where the raw files are stored.

## Next Steps :next_track_button:

**Data Collection**

Currently, files need to be manually downloaded from the website and placed into a folder. In the future, this should be an automated step. For instance, this could be orchestrated through [Airflow](https://airflow.apache.org/), where there's a daily process that checks the website for any new files, and if they exist, downloads them into a GCP Storage space and the following step cleans the data and upserts it into the database.

**Upserting**

This version of the code will skip over records if a match already exists in the database. Maybe it would be more appropiate to have an upsert process.

**Full data integration**

For this excercise, only a subset of the data was used. However, there is more data in the datasources that could be added to the project.

**Improved network settings on GCP**

At the moment, the API and database are publicly accessible. However, it would be better to set them behind a firewall to only accept traffic through a VPN.