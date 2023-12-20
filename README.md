# Robopety
Our project aim is to set up a secure Web Application (on Google Cloud Platform) which acts as the central hub for people looking to buy robot pets. If the project is successful we will be able to provide a safe platform for users to buy robo pets.


## Run Locally

Clone the project

```bash
  git clone https://github.com/SyedFaquar/Robopety.git
```

Go to the project directory

```bash
  cd Robopety-main
```

Install dependencies

```bash
   pip install -r requirements. txt
```

Start the server

```bash
  python3 main.py
  python main.py
```


## Deployment

To deploy this project on Google Cloud App Engine:

Install the Google CLI: 

```bash
  https://cloud.google.com/sdk/docs/install
```


Initialize the gcloud CLI, run the following command:

```bash
  gcloud init
```
To deploy the web service, you run the gcloud app deploy command from the root directory of your project, where your app.yaml file is located:

```bash
  gcloud app deploy
```

To connect this project with Google Cloud SQL:

Make sure the Google Cloud SQL instance enabled the API and public IP for Google Cloud Proxy connection

Robopety connects to the Google Cloud SQL through API calls in the

```bash
  database.py
```

The following values are required to establish the connection with the Google Cloud Proxy and stored in the environmental variables defined in the app.yaml file:

```bash
  CLOUD_SQL_USERNAME
  CLOUD_SQL_PASSWORD
  CLOUD_SQL_DATABASE_NAME
  CLOUD_SQL_CONNECTION_NAME
```

To connect Robopety with the Google Cloud Storage:

The following information is required

```bash
  BUCKET_NAME
```

This value is stored in the environmental varialbe defined in the app.yaml file


## Environment Variables

To run this project, you will need to add the following environment variables to your app.yaml file:

`CLOUD_SQL_USERNAME`: username of the user to connect the Google Cloud SQL instance

`CLOUD_SQL_PASSWORD`: password of the user to connect the Google Cloud SQL instance

`CLOUD_SQL_DATABASE_NAME`: the name of the target database in the Google Cloud SQL instance

`CLOUD_SQL_CONNECTION_NAME`: the connection name of the Google Cloud SQL instance

`BUCKET_NAME`: the name of the target bucket in Google Cloud Storage

`JWT_SECRET`: the secret used in encoding the jwt token






