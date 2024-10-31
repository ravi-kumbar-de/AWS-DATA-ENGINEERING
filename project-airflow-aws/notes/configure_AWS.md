# Configure AWS to run this project

## 1. Create an AWS IAM user
On _IAM dashboard_, I created the user `awsuser` with permissions:
- `AdministrationAccess`
- `AmazonRedshiftFullAccess`
- `AmazonS3FullAccess`


## 2. Create a Role to manage Redshift
On **AWS Cloudshell**, I created the role `my-redshift-service-role` _to manage_ **Redshift**.
```
aws iam create-role --role-name my-redshift-service-role --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "redshift.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}'
```

Now give the role _S3 Full Access_:

`aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name my-redshift-service-role`

### 3. Configure Redshift Serverless in AWS
> Based on this [Udacity lesson](https://learn.udacity.com/nanodegrees/nd027/parts/cd12380/lessons/a0015ec8-9e09-4189-8275-6c715b42aa4c/concepts/bc3bd8dc-3b03-41f3-8e65-f30a3a6688ea).

#### Create a Redshift servless workspace and namespace
- Open the AWS console by clicking on the Launch Cloud Gateway button followed the Open Cloud Console button in the classroom.
- Search Redshift in the search bar, and then click on Amazon Redshift.
- On the left click the hamburger menu
- Click Redshift Serverless
- Click Customize settings
- Create workgroup
  - workgroup name: default
  - Keep the default network and security options
  - Turn on enhanced VPC routing
  - Next
- Namespace
  - Name: default
  - Database name and password
    - Database name: dev
    - Password: one of your preference
  - Associated IAM roles
    - Associate IAM role
      - Choose: `my-redshift-service-role`

#### Make your _workspace_ **publicly accessible**:
> This is important to connect to this _cluster_ via _Airflow_, otherwise, Airflow won't be able to connect!
- On the **Workspace page**
  - Edit network and security > Turn on Publicly accessible

#### Create an _inbound rule_
> Choose the link labeled **VPC security group** to open the Amazon Elastic Compute Cloud (Amazon EC2) console.
- On Workspace propertites > Data access tab
  - Click on VPC security group
    - Go to Inbound Rules tab and click on Edit inbound rules.
      - Add an inbound rule, as shown in the image below.
      - Type = Custom TCP
      - Port range = 0 - 5500
      - Source = Anywhere-iPv4

Now Redshift Serverless should be accessible from Airflow.

