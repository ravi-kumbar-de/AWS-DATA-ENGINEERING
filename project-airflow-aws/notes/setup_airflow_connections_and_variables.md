# Setup Airflow Connections and Variables

## 1. Setup connections between Airflow and AWS
- Go to the **Airflow UI**
- Menu > Admin > Connections
- Click the plus button to create a new connection

### 1.1. IAM connection
- **Connection Id:** `aws_credentials`
- **Connection Type:** Enter Amazon Web Services.
- **AWS Access Key ID:** Enter your Access key ID from the IAM User credentials you downloaded earlier.
- **AWS Secret Access Key:** Enter your Secret access key from the IAM User credentials you downloaded earlier.
- Test
- Save

> **Note:** The Access key ID and Secret access key should be taken from the csv file you downloaded after creating an IAM User on the page Create an IAM User in AWS.

### 1.2. Connect Airflow to AWS Redshift Serverless
> Adapted from this [link](https://learn.udacity.com/nanodegrees/nd027/parts/cd12380/lessons/a0015ec8-9e09-4189-8275-6c715b42aa4c/concepts/72cd3a11-791b-4467-a273-7e26b713a968)
- **Connection Id:** `redshift`
- **Connection Type:** Amazon Redshift
**Host:** Enter the endpoint of your Redshift Serverless workgroup, excluding the port and schema name at the end. You can find this by selecting your workgroup in the Amazon Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to NOT include the port and schema name at the end of the Redshift endpoint string.
- **Schema:** `dev`. This is the Redshift database you want to connect to.
- **Login:** Enter YOUR USERNAME.
- **Password: Enter the password you created when launching Redshift serverless.
- **Port:** `5439`.
- Test
- Save

## 2. Setting Airflow Environment Variables for the project
One good way to avoid exposing _sensitive information_ in your python code is to "hide them" as **Airflow environment variables**. This alternative is also good for frequently used information.

To add a new **variable** in **Airflow**:
- On Airflow UI
- Menu > Admin > Variables
- Click the plus button

The variables used in this project are:
  - **Key:** region, **Val:** us-west-2
  - **Key:** s3_bucket, **Val:** udacity-dend
  - **Key:** s3_prefix_log_data, **Val:** log_data
  - **Key:** s3_prefix_log_json_path, **Val:** log_json_path.json
  - **Key:** s3_prefix_song_data, **Val:** song_data


Once set up, we can access them in our python code by:
```
from airflow.models import Variable

YOUR_variable = Variable.get('YOUR_VARIABLE_NAME'))
```

To test, check and run the python script: `test/list_airflow_variables.py`

