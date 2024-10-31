import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house-samucoding/accelerometer/landing/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerLanding_node1",
)

# Script generated for node Customer Trusted
CustomerTrusted_node1690252307671 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house-samucoding/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="CustomerTrusted_node1690252307671",
)

# Script generated for node Customer Privacy Filter
CustomerPrivacyFilter_node1690252648193 = Join.apply(
    frame1=CustomerTrusted_node1690252307671,
    frame2=AccelerometerLanding_node1,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="CustomerPrivacyFilter_node1690252648193",
)

# Script generated for node Privacy Filter by Date
SqlQuery0 = """
SELECT * FROM accelerometer_landing_customer_trusted_data WHERE FROM_UNIXTIME(timeStamp / 1000e0) > FROM_UNIXTIME(shareWithResearchAsOfDate / 1000e0);
"""
PrivacyFilterbyDate_node1690252694629 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={
        "accelerometer_landing_customer_trusted_data": CustomerPrivacyFilter_node1690252648193
    },
    transformation_ctx="PrivacyFilterbyDate_node1690252694629",
)

# Script generated for node Drop Fields
DropFields_node1690253124251 = DropFields.apply(
    frame=PrivacyFilterbyDate_node1690252694629,
    paths=[
        "shareWithFriendsAsOfDate",
        "phone",
        "lastUpdateDate",
        "email",
        "customerName",
        "shareWithResearchAsOfDate",
        "registrationDate",
        "birthDay",
        "shareWithPublicAsOfDate",
        "serialNumber",
    ],
    transformation_ctx="DropFields_node1690253124251",
)

# Script generated for node Drop Duplicates
DropDuplicates_node1690397581991 = DynamicFrame.fromDF(
    DropFields_node1690253124251.toDF().dropDuplicates(),
    glueContext,
    "DropDuplicates_node1690397581991",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropDuplicates_node1690397581991,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-lake-house-samucoding/accelerometer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="AccelerometerTrusted_node3",
)

job.commit()
