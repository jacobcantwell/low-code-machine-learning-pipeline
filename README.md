# low-code-machine-learning-pipeline

A Low Code AWS Machine Learning Pipeline

## Data Format of the Call Data Records

Below is the list of columns in our data set.

| Source key | Data example |
| ----------- | ----------- |
| start_datetime | 25-02-2021 11:53 | 
| translated_calling_number | 4712226680853 | 
| translated_called_number | 4712226680853 | 
| connect_datetime | 25-02-2021 11:53 | 
| disconnect_datetime | 25-02-2021 12:48 | 
| charged_duration | 55 | 
| originating_carrier_id | 6 | 
| originating_transit_carrier_id | 6 | 
| terminating_carrier_id | 4 | 
| terminating_transit_carrier_id | 4 | 
| call_direction | 1 |

```csv
start_datetime,translated_calling_number,translated_called_number,connect_datetime,disconnect_datetime,charged_duration,originating_carrier_id,originating_transit_carrier_id,terminating_carrier_id,terminating_transit_carrier_id,call_direction
25-02-2021 11:53,5893746421295,5893746421295,25-02-2021 11:53,25-02-2021 12:48,55,7,7,8,8,1
04-03-2022 10:05,4767306697766,4767306697766,04-03-2022 10:05,04-03-2022 10:18,13,3,3,0,0,2
14-05-2022 11:05,6632467120375,6632467120375,14-05-2022 11:05,14-05-2022 11:28,23,3,3,9,9,2
```

Dates are provided in the format `%d-%m-%Y %H:%M`

We want to transform this data with the following mappings

| Source key | Transform |
| ----------- | ----------- |
| start_datetime | *Data type* to `timestamp` |
| connect_datetime | *Data type* to `timestamp` |
| disconnect_datetime | *Data type* to `timestamp` |
| originating_transit_carrier_id | select `Drop` |
| terminating_transit_carrier_id | select `Drop` |

## AWS Resources

Follow these steps to create the required AWS resources.

## Amazon S3

[Amazon S3](https://aws.amazon.com/s3/) is object storage built to store and retrieve any amount of data from anywhere. It’s a simple storage service that offers industry leading durability, availability, performance, security, and virtually unlimited scalability at very low costs.

### Create an Amazon S3 bucket

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

## AWS Glue

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

## AWS Glue Studio

AWS Glue Studio makes it easier to visually create, run, and monitor AWS Glue ETL jobs. You can build ETL jobs that move and transform data using a drag-and-drop editor, and AWS Glue automatically generates the code.

### Create a Glue Job IAM Role

All AWS services or users need AWS IAM permissions to be able to any resources on AWS. We will be creating an AWS Glue job that needs an IAM role with permission to extract data from your data source, write data to your target, and access AWS Glue resources.

The name of the role that you create for the job must start with the string *AWSGlueServiceRole* for it to be used correctly by AWS Glue Studio. For example, you might name your role *AWSGlueServiceRole-MockData*.

* Search for `IAM` in the Amazon Management Console
* Select `IAM`
* Select `Roles`
* Select `Create role`
* For role type, choose AWS Service, find and choose `Glue`, and choose `Next: Permissions`.
* On the Attach permissions policy page, choose the policies that contain the required permissions. For example, you might choose the AWS managed policy `AWSGlueServiceRole` for general AWS Glue Studio and AWS Glue permissions and the AWS managed policy `AmazonS3FullAccess` for access to Amazon S3 resources.
  * Add additional policies as needed for additional data stores or services.
* Choose `Next: Review`.
* For Role name, enter a name for your role; for example, `AWSGlueServiceRole-MockData`. Choose a name that begins with the string AWSGlueServiceRole to allow the role to be passed from console users to the service. 

### Create a Glue Job

* Search for `Glue` in the Amazon Management Console
* Select `AWS Glue Studio`
* Select `Jobs`
* Create job
  * Select `Visual with a blank canvas`
  * Select `Create`
* Rename Untitled job `call-detail-records-transform-job-v1`
* Create a data *Source*
  * Select `Source`
  * Select `Amazon S3`
  * S3 source type, select `Data Catalog table`
  * Database, select `call-detail-records-mock-database`
  * Table, select `raw`

* Create a data *Action*
  * Select the `Transform - ApplyMapping` node
  * Select `Action`
  * Select `SQL Query`
  * Select `Transform` tab
  * Insert the SQL query below

```sql
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
```

* Select `Output schema`
  * Edit *start_datetime* data type to `timestamp`
  * Edit *connect_datetime* data type to `timestamp`
  * Edit *disconnect_datetime* data type to `timestamp`
* Select `Data preview` to check that the datetime fields are populated and now in the timestamp format *yyyy-MM-dd HH:mm:SS*

* Create a data *Target*
  * Select the `Transform - SQL Query` node
  * Select `Target`
  * Select `Amazon S3`
  * Format `Parquet`
  * Compression Type `Snappy`
  * S3 Target Location `s3://call-detail-records-mock/processed-timestamp-v1/`
  * Data Catalog update options `Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions`
  * Database, select `call-detail-records-mock-database`
  * Table name `processed-timestamp-v1`
* Select top tab `Job details`
  * IAM Role, select the role you created above `AWSGlueServiceRole-MockData`
  * Job timeout (minutes) `10`
  * Job bookmark - `Disable` for this development environment so that all data is always processed
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

### View your AWS Glue Script

You can view the script generated by AWS Glue Studio by choosing the Script tab. The entire script is displayed in a locked, read-only format by default. You can choose Edit script to unlock the script for editing.

If you choose to edit the script, the job authoring experience is permanently converted to a script-only mode. Afterwards, you cannot use the visual editor to edit the job anymore.

You should add all the job sources, transforms, and targets, and make all the changes you require with the visual editor before choosing to edit the script.

### Schedule an AWS Glue job

* Select `Schedules`
* Select `Create schedule`
* Enter a name `call-detail-records-hourly-schedule-v1`
* Select `Create schedule`

### Monitoring a AWS Glue job

* Select `Monitoring`
* Review the job run dashboard
* Select your job run and select `View job`

## Amazon Athena

Amazon Athena is an interactive query service that makes it easy to analyze data directly in Amazon Simple Storage Service (Amazon S3) using standard SQL. With a few actions in the AWS Management Console, you can point Athena at your data stored in Amazon S3 and begin using standard SQL to run ad-hoc queries and get results in seconds. Athena is serverless, so there is no infrastructure to setup or manage, and you can start analyzing data immediately.

Amazon Athena can be used as a data source for business intelligence tools and other applications, such as SQL workbench. To explore and visualize your data with business intelligence tools, download, install, and configure an ODBC (Open Database Connectivity) or JDBC (Java Database Connectivity) driver. On Windows operating systems, you can use the Microsoft Power BI connector for Amazon Athena to analyze data from Amazon Athena in Microsoft Power BI Desktop. Athena integrates with Amazon QuickSight for easy data visualization in the AWS management console.

### Setup Amazon Athena

The first time you have used Amazon Athena in your AWS account, you will need to setup the Query result location.
* Select `Settings`
* Select `Manage`
* Enter a location of query results

### Query Data with Amazon Athena

* Search for `Athena` in the Amazon Management Console
* Under *Tables and views*, expand your new table `processed`. You should see all of the data columns with new timestamp formats.
* Select the vertical `...` menu
* Select `Preview Table`

This will create an SQL query that and you can preview data sitting in Amazon S3 and cataloged and transformed with AWS Glue.

```
SELECT * FROM "call-detail-records-mock-database"."processed" limit 10;
```

## Amazon Quicksight

Amazon QuickSight is a very fast, easy-to-use, cloud-powered business analytics service that makes it easy for all employees within an organization to build visualizations, perform ad-hoc analysis, and quickly get business insights from their data, anytime, on any device. Upload CSV and Excel files; connect to SaaS applications like Salesforce; access on-premises databases like SQL Server, MySQL, and PostgreSQL; and seamlessly discover your AWS data sources such as Amazon Redshift, Amazon RDS, Amazon Aurora, Amazon Athena, and Amazon S3. QuickSight enables organizations to scale their business analytics capabilities to hundreds of thousands of users, and delivers fast and responsive query performance by using a robust in-memory engine (SPICE).

### Manage Amazon QuickSight

* Search for `QuickSight` in the Amazon Management Console
* Click on person icon on the top right hand of the QuickSight console
* Select `Security & permissions`
* Under *QuickSight access to AWS services*, select `Manage`
* Check the *Amazon S3* checkbox
* Select `Select S3 buckets`
* Check the box for the Amazon S3 bucket with the processed data `call-detail-records-mock`
* Select `Finish`

### Create Amazon QuickSight Dataset

When you import data into a dataset rather than using a direct SQL query, it becomes SPICE data because of how it's stored. SPICE (Super-fast, Parallel, In-memory Calculation Engine) is the robust in-memory engine that Amazon QuickSight uses. It's engineered to rapidly perform advanced calculations and serve data. In Enterprise edition, data stored in SPICE is encrypted at rest.

You will create a new SPICE dataset based on an Amazon S3.

* Select `Datasets`
* Select `New Dataset`
* Select `Athena`
* Enter a name for the data source `processed-timestamp-v1`
* Select `Create data source`
* Select the AWS Glue Catalog `AwsDataCatalog`
* Select the AWS Glue Database `call-detail-records-mock-database`
* Select the process data table created by your AWS Glue ETL job `processed-timestamp-v1`
* Select `Select`
* Select `Import to SPICE for quicker analytics`
* Select `Visualize`

Your data will be imported to SPICE and you can start creating visualizations.

#### Create calculated fields

You can add calculated fields to a dataset during data preparation or from the analysis page. When you add a calculated field to a dataset during data preparation, it's available to all analyses that use that dataset.

Add the calculated fields below.

* Open your analysis
* Select `+ Add` dropdown and `Add calculated field`
* Enter a name using the table below
* Enter a formula using the table below
* Select `Save`

| Field name | Formula |
| -- | -- |
| total charge | {day charge} + {evening charge} + {night charge} |
| total minutes | {day minutes} + {evening minutess} + {night minutes} |

Review the data set to see of the fields including the new calculated fields.

* Select `Datasets`
* Select dataset `processed-timestamp-v1`
* Select `EDIT DATASET`



### Create a Visualization

#### Creating a new visual

* Select `Add visual`
* Select the new AutoGraph chart
* Select the visual type
* Drag the fields to your chart
* Resize the chart as necessary

#### Example Visuals

| Chart Title | Chart type | Value | Target value measure | Trend group dimension | Filter | Sort |
| -- | -- | -- | -- | -- | -- | -- |
| Sum of Total Minutes | Autograph | total minutes (Sum) | - | - | - | - |
| Sum of Total Charge | Autograph | total charge (Sum) | - | - | - | - |
| Sum of Minutes by Type | Vertical bar chart | day minutes (Sum)<br />evening minutes (Sum)<br />night minutes (Sum)<br /> | - | - | - | - |
| Sum of Minutes Type by Phone Number | Vertical bar chart | phone number | - | day minutes (Sum)<br />evening minutes (Sum)<br />night minutes (Sum)<br /> | phone number, top and bottom filter, top 10 by total minutes Sum | total minutes descending |

