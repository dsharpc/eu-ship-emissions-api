# EU Ship Emissions API :ship:

This repository contains the code for an API that serves data from the [THETIS-MRV dataset](https://mrv.emsa.europa.eu/#public/emission-report) which contains emissions data for ships larger than 5,000 tons that dock in the EU.

## Setup Requirements :gear:

At the moment, the project's data files were manually downloaded from the website and saved into a GCP Cloud Storage Bucket, which were made public. However, if new data was to be added, the same manual step would have to be repeated. See the **Next steps** section below for some potential next steps to improve this process.

## Execution :rocket:
The API is built using the FastAPI Python library. The data is stored in a PostgreSQL database. Both services are run using Docker containers and coordinated through Docker Compose.

To start the services, run the following command:

```
docker compose up -d 
```

This will build the Docker files and start the two services. You can verify the correct startup through the `docker compose ps` command and by opening a browser and going to `localhost:8000/docs`, which will show the Swagger docs for the API.


## Next Steps :next_track_button:

**Data Collection**

Currently, files need to be manually downloaded from the website and placed into a folder. In the future, this should be an automated step. For instance, this could be orchestrated through [Airflow](https://airflow.apache.org/), where there's a daily process that checks the website for any new files, and if they exist, downloads them into a GCP Storage space and the following step cleans the data and upserts it into the database.
