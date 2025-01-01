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

# Script generated for node Customer Curated
CustomerCurated_node1729964687469 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi_db",
    table_name="customer_curated",
    transformation_ctx="CustomerCurated_node1729964687469",
)

# Script generated for node Step Trainer Landing
StepTrainerLanding_node1729964742532 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiLine": "false"},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://stedi-project/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainerLanding_node1729964742532",
)

# Script generated for node Renamed keys for Join
RenamedkeysforJoin_node1729965162691 = ApplyMapping.apply(
    frame=StepTrainerLanding_node1729964742532,
    mappings=[
        ("sensorreadingtime", "bigint", "sensorreadingtime", "long"),
        ("serialnumber", "string", "right_serialnumber", "string"),
        ("distancefromobject", "int", "right_distancefromobject", "int"),
    ],
    transformation_ctx="RenamedkeysforJoin_node1729965162691",
)

# Script generated for node Join
Join_node1729965132289 = Join.apply(
    frame1=CustomerCurated_node1729964687469,
    frame2=RenamedkeysforJoin_node1729965162691,
    keys1=["serialnumber"],
    keys2=["right_serialnumber"],
    transformation_ctx="Join_node1729965132289",
)

# Script generated for node Drop Fields
DropFields_node1729965187338 = DropFields.apply(
    frame=Join_node1729965132289,
    paths=[
        "registrationdate",
        "birthday",
        "customername",
        "sharewithfriendsasofdate",
        "sharewithpublicasofdate",
        "lastupdatedate",
        "email",
        "phone",
        "sharewithresearchasofdate",
        "serialnumber",
    ],
    transformation_ctx="DropFields_node1729965187338",
)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1729965247885 = glueContext.getSink(
    path="s3://stedi-project/step_trainer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="StepTrainerTrusted_node1729965247885",
)
StepTrainerTrusted_node1729965247885.setCatalogInfo(
    catalogDatabase="stedi_db", catalogTableName="step_trainer_trusted"
)
StepTrainerTrusted_node1729965247885.setFormat("json")
StepTrainerTrusted_node1729965247885.writeFrame(DropFields_node1729965187338)
job.commit()
