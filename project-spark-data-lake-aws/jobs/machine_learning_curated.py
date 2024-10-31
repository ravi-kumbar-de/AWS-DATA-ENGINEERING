import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house-samucoding/step_trainer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainerTrusted_node1",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1690334760836 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-lake-house-samucoding/accelerometer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerTrusted_node1690334760836",
)

# Script generated for node ML Join Data
MLJoinData_node1690334781668 = Join.apply(
    frame1=StepTrainerTrusted_node1,
    frame2=AccelerometerTrusted_node1690334760836,
    keys1=["sensorReadingTime"],
    keys2=["timeStamp"],
    transformation_ctx="MLJoinData_node1690334781668",
)

# Script generated for node ML Curated
MLCurated_node3 = glueContext.write_dynamic_frame.from_options(
    frame=MLJoinData_node1690334781668,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://stedi-lake-house-samucoding/machine_learning/curated/",
        "partitionKeys": [],
    },
    transformation_ctx="MLCurated_node3",
)

job.commit()
