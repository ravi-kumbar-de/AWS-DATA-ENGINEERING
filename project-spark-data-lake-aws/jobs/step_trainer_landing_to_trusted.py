import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Step Trainer Landing
StepTrainerLanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house-samucoding/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainerLanding_node1",
)

# Script generated for node Customer Curated
CustomerCurated_node1690332858706 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house-samucoding/customer/curated/"],
        "recurse": True,
    },
    transformation_ctx="CustomerCurated_node1690332858706",
)

# Script generated for node Renamed keys for Privacy Filter
RenamedkeysforPrivacyFilter_node1690332994920 = ApplyMapping.apply(
    frame=CustomerCurated_node1690332858706,
    mappings=[
        ("serialNumber", "string", "right_serialNumber", "string"),
        ("shareWithPublicAsOfDate", "bigint", "shareWithPublicAsOfDate", "long"),
        ("shareWithResearchAsOfDate", "bigint", "shareWithResearchAsOfDate", "long"),
        ("registrationDate", "bigint", "registrationDate", "long"),
        ("lastUpdateDate", "bigint", "lastUpdateDate", "long"),
        ("shareWithFriendsAsOfDate", "bigint", "shareWithFriendsAsOfDate", "long"),
    ],
    transformation_ctx="RenamedkeysforPrivacyFilter_node1690332994920",
)

# Script generated for node Privacy Filter
PrivacyFilter_node1690332917934 = Join.apply(
    frame1=StepTrainerLanding_node1,
    frame2=RenamedkeysforPrivacyFilter_node1690332994920,
    keys1=["serialNumber"],
    keys2=["right_serialNumber"],
    transformation_ctx="PrivacyFilter_node1690332917934",
)

# Script generated for node Drop Customer Fields
DropCustomerFields_node1690333043810 = DropFields.apply(
    frame=PrivacyFilter_node1690332917934,
    paths=[
        "right_serialNumber",
        "shareWithPublicAsOfDate",
        "shareWithResearchAsOfDate",
        "registrationDate",
        "lastUpdateDate",
        "shareWithFriendsAsOfDate",
    ],
    transformation_ctx="DropCustomerFields_node1690333043810",
)

# Script generated for node Drop Duplicates
DropDuplicates_node1690333060598 = DynamicFrame.fromDF(
    DropCustomerFields_node1690333043810.toDF().dropDuplicates(),
    glueContext,
    "DropDuplicates_node1690333060598",
)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1690333127288 = glueContext.write_dynamic_frame.from_options(
    frame=DropDuplicates_node1690333060598,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-lake-house-samucoding/step_trainer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="StepTrainerTrusted_node1690333127288",
)

job.commit()
