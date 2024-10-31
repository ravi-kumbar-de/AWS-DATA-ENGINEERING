## Configure the S3 Gateway Endpoint
### Find your VPC ID and Routing Table ID
On _AWS CLI_
- run `aws ec2 describe-vpcs` and copy the value for the `"VpcId"` key.
- run `aws ec2 describe-route-tables` and copy the value for the `"RouteTableId"` key.

### Create a S3 Gateway Endpoint
`aws ec2 create-vpc-endpoint --vpc-id vpc-XXXXXXX --service-name com.amazonaws.us-east-1.s3 --route-table-ids rtb-XXXXXXXX`

**Notes:**
- Replace `vpc-XXXXXXX` with your _VPC ID_ and `rtb-XXXXXXXX` with you _Routing Table ID_.
- Note that the **service name** contains the _region_ (`us-east-1`) and the _service_ desired to create the endpoint (`s3`): `com.amazonaws.us-east-1.s3`

### Check the created **S3 Gateway Endpoint**
- Go to the **VPC Dashboard** on **AWS**.
- Be sure you selected the _same region_ where you created the endpoint
- Click on **Endpoints**
- See the created _S3 Gateway Endpoint_


## Create a Glue Service IAM Role to manage Glue
### Create an IAM Role with access to AWS Glue
```
aws iam create-role --role-name my-glue-service-role --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "glue.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}'
```
- Inspect the created role on **IAM dashboard**

### Grant Glue Privileges on your _S3 Bucket_ (Put Role Policy on a Role)
```
aws iam put-role-policy --role-name my-glue-service-role --policy-name S3Access --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListObjectsInBucket",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR-S3-BUCKET-NAME"
            ]
        },
        {
            "Sid": "AllObjectActions",
            "Effect": "Allow",
            "Action": "s3:*Object",
            "Resource": [
                "arn:aws:s3:::YOUR-S3-BUCKET-NAME/*"
            ]
        }
    ]
}'
```
- Replace `YOUR-S3-BUCKET-NAME` with your _bucket name_
- Inspect the _permissions/policies_ of this role on **IAM dashboard**


** Grant more Glue permissions
Last, **we need to give Glue *access to data* in special S3 buckets used for Glue configuration, and several other resources**.
```
aws iam put-role-policy --role-name my-glue-service-role --policy-name GlueAccess --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "glue:*",
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:ListAllMyBuckets",
                "s3:GetBucketAcl",
                "ec2:DescribeVpcEndpoints",
                "ec2:DescribeRouteTables",
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcAttribute",
                "iam:ListRolePolicies",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "cloudwatch:PutMetricData"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:PutBucketPublicAccessBlock"
            ],
            "Resource": [
                "arn:aws:s3:::aws-glue-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::aws-glue-*/*",
                "arn:aws:s3:::*/*aws-glue-*/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::crawler-public*",
                "arn:aws:s3:::aws-glue-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:AssociateKmsKey"
            ],
            "Resource": [
                "arn:aws:logs:*:*:/aws-glue/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Condition": {
                "ForAllValues:StringEquals": {
                    "aws:TagKeys": [
                        "aws-glue-service-resource"
                    ]
                }
            },
            "Resource": [
                "arn:aws:ec2:*:*:network-interface/*",
                "arn:aws:ec2:*:*:security-group/*",
                "arn:aws:ec2:*:*:instance/*"
            ]
        }
    ]
}'
```
- Inspect the _permissions/policies_ of this role on **IAM dashboard**

