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

# Script generated for node Customer Trusted
CustomerTrusted_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house-samucoding/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="CustomerTrusted_node1",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1690329778730 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house-samucoding/accelerometer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerTrusted_node1690329778730",
)

# Script generated for node Customer with Accelerometer Readings Filter
CustomerwithAccelerometerReadingsFilter_node1690329966489 = Join.apply(
    frame1=CustomerTrusted_node1,
    frame2=AccelerometerTrusted_node1690329778730,
    keys1=["email"],
    keys2=["user"],
    transformation_ctx="CustomerwithAccelerometerReadingsFilter_node1690329966489",
)

# Script generated for node Drop Accelerometer Fields
DropAccelerometerFields_node1690330031500 = DropFields.apply(
    frame=CustomerwithAccelerometerReadingsFilter_node1690329966489,
    paths=["timeStamp", "z", "user", "y", "x"],
    transformation_ctx="DropAccelerometerFields_node1690330031500",
)

# Script generated for node Drop Duplicates
DropDuplicates_node1690330176425 = DynamicFrame.fromDF(
    DropAccelerometerFields_node1690330031500.toDF().dropDuplicates(),
    glueContext,
    "DropDuplicates_node1690330176425",
)

# Script generated for node Anonymization
Anonymization_node1690330223484 = DropFields.apply(
    frame=DropDuplicates_node1690330176425,
    paths=["email", "phone", "customerName", "birthDay"],
    transformation_ctx="Anonymization_node1690330223484",
)

# Script generated for node Customer Curated
CustomerCurated_node3 = glueContext.write_dynamic_frame.from_options(
    frame=Anonymization_node1690330223484,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-lake-house-samucoding/customer/curated/",
        "partitionKeys": [],
    },
    transformation_ctx="CustomerCurated_node3",
)

job.commit()
