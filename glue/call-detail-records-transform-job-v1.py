import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


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
AmazonS3_node1668643750596 = glueContext.create_dynamic_frame.from_catalog(
    database="call-detail-records-mock-database",
    table_name="raw-d-m-y-raw_format_d_m_y",
    transformation_ctx="AmazonS3_node1668643750596",
)

# Script generated for node SQL Query
SqlQuery36 = """
select
  to_timestamp(start_datetime,'dd-MM-yyyy HH:mm') AS start_datetime,
  translated_calling_number,
  translated_called_number, 
  to_timestamp(connect_datetime,'dd-MM-yyyy HH:mm') AS connect_datetime,
  to_timestamp(disconnect_datetime,'dd-MM-yyyy HH:mm') AS disconnect_datetime,
  charged_duration,
  originating_carrier_id,
  terminating_carrier_id,
  call_direction
from myDataSource
"""
SQLQuery_node1668643866929 = sparkSqlQuery(
    glueContext,
    query=SqlQuery36,
    mapping={"myDataSource": AmazonS3_node1668643750596},
    transformation_ctx="SQLQuery_node1668643866929",
)

# Script generated for node Amazon S3
AmazonS3_node1668644598459 = glueContext.getSink(
    path="s3://call-detail-records-mock/processed-timestamp-v1/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1668644598459",
)
AmazonS3_node1668644598459.setCatalogInfo(
    catalogDatabase="call-detail-records-mock-database",
    catalogTableName="processed-timestamp-v1",
)
AmazonS3_node1668644598459.setFormat("glueparquet")
AmazonS3_node1668644598459.writeFrame(SQLQuery_node1668643866929)
job.commit()
