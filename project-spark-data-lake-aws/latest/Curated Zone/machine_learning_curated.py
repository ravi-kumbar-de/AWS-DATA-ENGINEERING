import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1729979565750 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi_db",
    table_name="accelerometer_trusted",
    transformation_ctx="AccelerometerTrusted_node1729979565750",
)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1729974956681 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi_db",
    table_name="step_trainer_trusted",
    transformation_ctx="StepTrainerTrusted_node1729974956681",
)

# Script generated for node Join
Join_node1729979630657 = Join.apply(
    frame1=AccelerometerTrusted_node1729979565750,
    frame2=StepTrainerTrusted_node1729974956681,
    keys1=["timestamp"],
    keys2=["right_sensorreadingtime"],
    transformation_ctx="Join_node1729979630657",
)

# Script generated for node Drop Fields
DropFields_node1729984320721 = DropFields.apply(
    frame=Join_node1729979630657,
    paths=["z", "user", "y", "x", "timestamp"],
    transformation_ctx="DropFields_node1729984320721",
)

# Script generated for node Machine Learning Curated
MachineLearningCurated_node1729984508155 = glueContext.getSink(
    path="s3://stedi-project/step_trainer/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="MachineLearningCurated_node1729984508155",
)
MachineLearningCurated_node1729984508155.setCatalogInfo(
    catalogDatabase="stedi_db", catalogTableName="machine_learning_curated"
)
MachineLearningCurated_node1729984508155.setFormat("json")
MachineLearningCurated_node1729984508155.writeFrame(DropFields_node1729984320721)
job.commit()
