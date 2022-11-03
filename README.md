# low-code-machine-learning-pipeline

A Low Code AWS Machine Learning Pipeline


## AWS Resources

Follow these steps to create the required AWS resources.

### Amazon S3 bucket

[Amazon S3](https://aws.amazon.com/s3/) is object storage built to store and retrieve any amount of data from anywhere. It’s a simple storage service that offers industry leading durability, availability, performance, security, and virtually unlimited scalability at very low costs.

Create an Amazon S3 bucket in your local AWS region (e.g. ap-southeast-2) to store the CDR files. Group files into Amazon S3 bucket files by their schema type, so files of one type should go in their own folder.

* Search for `S3` in the Amazon Management Console
* Create an Amazon S3 bucket in your local AWS region
  * Select `Create bucket`
  * Bucket name: `call-detail-records-mock`
  * AWS Region: `Asia Pacific (Sydney) ap-southeast-2`
  * Select `Create bucket`
* Create a folder for the data that you will be uploading
  * Select `Create folder`
  * Folder name `raw`
  * Select `Create folder`
* Select the `raw` folder
* Copy the CDR csv files from the [data](./data/) folder to your Amazon S3 bucket *raw* folder
  * Select your new bucket name `call-detail-records-mock`
  * Select `Upload`
  * Drag and drop files and folders you want to upload, or choose `Add files`
  * Select `Upload`
  * After the files have uploaded, select `Close`

### AWS Glue

[AWS Glue](https://aws.amazon.com/glue/) is a serverless data integration service that makes it easy to discover, prepare, and combine data for analytics, machine learning, and application development. AWS Glue provides all the capabilities needed for data integration, so you can start analyzing your data and putting it to use in minutes instead of months. AWS Glue provides both visual and code-based interfaces to make data integration easier. Users can easily find and access data using the AWS Glue Data Catalog. Data engineers and ETL (extract, transform, and load) developers can visually create, run, and monitor ETL workflows with a few clicks in AWS Glue Studio. Data analysts and data scientists can use AWS Glue DataBrew to visually enrich, clean, and normalize data without writing code.

### AWS Glue Crawler

An AWS Glue Crawler connects to a data store, progresses through a prioritized list of classifiers to determine the schema for your data, and then creates metadata tables in your data catalog.

You will create a crawler for each data schema type that you have organized into an Amazon S3 bucket.

* Search for `Glue` in the Amazon Management Console
* Select `Crawlers`
* Select `Create crawler`
* Set crawler properties
  * Enter a unique crawler name: `call-detail-records-mock-crawler`
  * Select `Next`
* Choose data sources and classifiers
  * Select `Add a data source`
* In the popup, Add data source
  * Data source `S3`
  * Enter the S3 path to your bucket `s3://call-detail-records-mock/raw/`
    * Path should end with a `/` character
  * Select `Add an S3 data source`
  * Select `Next`
* Configure security settings
  * Select `Create new IAM role`
  * Enter new IAM role `AWSGlueServiceRole-call-detail-records-mock`
  * Select `Create`
  * Make sure the new role is selected for the Existing IAM role
  * Select `Next`
* Set output and scheduling
  * Select `Add database`
  * Your web browser will open a new tab to the AWS Glue Create a database page
  * Enter a unique database name `call-detail-records-mock-database`
  * Select `Create database`
  * Return your web browser to the tab for Set output and scheduling
  * Select the refresh button next to Target database
  * Select the new database name `call-detail-records-mock-database`
  * Keep Frequency as `On demand`
  * Select `Next`
* Review and create
  * Select `Create crawler`
* Run the crawler
  * Select crawler name `call-detail-records-mock-crawler`
  * Select `Run crawler`
  * Crawler will start running and you can see its status at the bottom section Crawler runs

### AWS Glue Table

* View new AWS Glue table
  * Select `Databases`
  * Select database name `call-detail-records-mock-database`
  * Select table name `raw`
  * View and manage the table schema

You can see that the columns *start_datetime*, *connect_datetime*, and *disconnect_datetime* have the data type *string*. These fields need to be converted to the data type *timestamp* so that we can run time related searches.

### AWS Glue Studio

AWS Glue Studio makes it easier to visually create, run, and monitor AWS Glue ETL jobs. You can build ETL jobs that move and transform data using a drag-and-drop editor, and AWS Glue automatically generates the code.

* Search for `Glue` in the Amazon Management Console
* Select `AWS Glue Studio`
* Select `Jobs`
* Create job
  * Select `Visual with a source and target`
  * Source `Amazon S3`
  * Target `Amazon S3`
  * Select `Create`
* Rename Untitled job `call-detail-records-mock-transform-job`
* Select `Data source - S3 bucket`
  * S3 source type, select `Data Catalog table`
  * Database, select `call-detail-records-mock-database`
  * Table, select `raw`
* Select `Transform - ApplyMapping`
  * Select `Transform`

Apply the following mappings

| Source key | Transform |
| ----------- | ----------- |
| start_datetime | *Data type* to `timestamp` |
| connect_datetime | *Data type* to `timestamp` |
| disconnect_datetime | *Data type* to `timestamp` |
| originating_transit_carrier_id | select `Drop` |
| terminating_transit_carrier_id | select `Drop` |

* Select `Data target - S3 bucket`
  * Format `CSV`
  * Compression Type `Uncompressed`
  * S3 Target Location `s3://call-detail-records-mock/processed/`
  * Data Catalog update options `Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions`
  * Database, select `call-detail-records-mock-database`
  * Table name `processed`
* Select top tab `Job details`
  * IAM Role, select `AWSGlueServiceRole-call-detail-records-mock`
  * Advanced properties
  * Script filename `call-detail-records-mock-process.py`
* Select `Save`
* Select `Run`. Navigate to Run Details for more details.

* View new AWS Glue table
  * Select `Databases`
  * Select database name `call-detail-records-mock-database`
  * Select table name `processed`
  * View and manage the table schema

You can see that the columns *start_datetime*, *connect_datetime*, and *disconnect_datetime* have the data type *timestamp* and the *originating_transit_carrier_id* and *terminating_transit_carrier_id* columns have been removed.


### Amazon Athena

Amazon Athena is an interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. Athena is serverless, so there is no infrastructure to setup or manage, and you can start analyzing data immediately. You don’t even need to load your data into Athena, it works directly with data stored in S3.





