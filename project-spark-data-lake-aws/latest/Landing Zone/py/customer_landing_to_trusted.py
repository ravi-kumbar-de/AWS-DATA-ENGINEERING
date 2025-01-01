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

# Script generated for node Amazon S3
AmazonS3_node1729367858249 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiLine": "false"},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-project/customer/landing/"],
        "recurse": True,
    },
    transformation_ctx="AmazonS3_node1729367858249",
)

# Script generated for node SQL Query Filter
SqlQuery0 = """
select * from myDataSource where
sharewithresearchasofdate is not NULL
"""
SQLQueryFilter_node1729959393468 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={"myDataSource": AmazonS3_node1729367858249},
    transformation_ctx="SQLQueryFilter_node1729959393468",
)

# Script generated for node Trusted Customer Zone
TrustedCustomerZone_node1729369006039 = glueContext.getSink(
    path="s3://stedi-project/customer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="TrustedCustomerZone_node1729369006039",
)
TrustedCustomerZone_node1729369006039.setCatalogInfo(
    catalogDatabase="stedi_db", catalogTableName="customer_trusted"
)
TrustedCustomerZone_node1729369006039.setFormat("json")
TrustedCustomerZone_node1729369006039.writeFrame(SQLQueryFilter_node1729959393468)
job.commit()
