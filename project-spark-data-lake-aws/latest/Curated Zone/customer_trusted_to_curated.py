import sys

from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


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
AccelerometerLanding_node1729960501264 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi_db",
    table_name="accelerometer_landing",
    transformation_ctx="AccelerometerLanding_node1729960501264",
)

# Script generated for node Customer Trusted
CustomerTrusted_node1729960039481 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi_db",
    table_name="customer_trusted",
    transformation_ctx="CustomerTrusted_node1729960039481",
)

# Script generated for node Customer Privacy Filter
CustomerPrivacyFilter_node1729960129609 = Join.apply(
    frame1=CustomerTrusted_node1729960039481,
    frame2=AccelerometerLanding_node1729960501264,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="CustomerPrivacyFilter_node1729960129609",
)

# Script generated for node Drop Fields and Duplicates
SqlQuery0 = """
select distinct customername, email, phone, birthday,
serialnumber, registrationdate, lastupdatedate,
sharewithresearchasofdate, sharewithpublicasofdate,
sharewithfriendsasofdate from myDataSource
"""
DropFieldsandDuplicates_node1729962920911 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={"myDataSource": CustomerPrivacyFilter_node1729960129609},
    transformation_ctx="DropFieldsandDuplicates_node1729962920911",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1729960866737 = glueContext.getSink(
    path="s3://stedi-project/customer/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="AccelerometerTrusted_node1729960866737",
)
AccelerometerTrusted_node1729960866737.setCatalogInfo(
    catalogDatabase="stedi_db", catalogTableName="customer_curated"
)
AccelerometerTrusted_node1729960866737.setFormat("json")
AccelerometerTrusted_node1729960866737.writeFrame(
    DropFieldsandDuplicates_node1729962920911
)
job.commit()
