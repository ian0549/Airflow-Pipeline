# Data Pipeline with Airflow

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.


## Project Overview

This project will introduce you to the core concepts of Apache Airflow. To complete the project, you will need to create your own custom operators to perform tasks such as staging the data, filling the data warehouse, and running checks on the data as the final step.


## Airflow DAG  Configurations

In the DAG, add default parameters according to these guidelines

- The DAG does not have dependencies on past runs
- On failure, the task are retried 3 times
- Retries happen every 5 minutes
- Catchup is turned off
- Do not email on retry

**The graph view below shows the flow of the configuration of the task dependencies.**

![alt text](/airflow_pipeline.png)


## Project Files

Project contains 3 directories named dags , plugins and redshift

- create_tables.sql: SQL create table statements provided with template.

- dags directory contains:

   - sparkify_etl_dag.py: Defines main DAG, tasks and link the tasks in required order.

- plugins/operators directory contains:

   - stage_redshift.py: Defines StageToRedshiftOperator to copy JSON data from S3 to staging tables in the Redshift via copy command.
   - load_dimension.py: Defines LoadDimensionOperator to load a dimension table from staging table(s).
   - load_fact.py: Defines LoadFactOperator to load fact table from staging table(s).
   - data_quality.py: Defines DataQualityOperator to run data quality checks on all tables passed as parameter.
   - sql_queries.py: Contains SQL queries for the ETL pipeline .


- redshift directory contains:

   - aws_config.cfg: Aws configuration for seting up the redshift cluster
   - start_clusters.py: Python script for executing and launching redshift


# How to Setup Project

## Requirements

- Python 3 or later
- Airflow
- Boto3
- Pandas


## Project Configuration

- Create a Redshift Cluster

- Configure Airflow for running the DAGS


### Spin-Up Redshift

- Login to AWS console and create an IAM-user(Programmatic Access)

- Enter the credentials in the redshift/aws_config.cfg file

- Run the following in your terminal to spin up redshift clusters:
	```
	$python start_clusters.py
	```


### Configure Airflow

Here, we'll use Airflow's UI to configure your AWS credentials and connection to Redshift.

1. To go to the Airflow UI:

  - You can use the Project Workspace here and click on the blue Access Airflow button in the bottom right.
  
  - If you'd prefer to run Airflow locally, open http://localhost:8080 in Google Chrome (other browsers occasionally have issues rendering the Airflow UI).

2. Click on the Admin tab and select Connections.

3. Under Connections, select Create.

4. On the create connection page, enter the following values:

   - Conn Id: Enter aws_credentials.
   
   - Conn Type: Enter Amazon Web Services.
   
   - Login: Enter your Access key ID from the IAM User credentials you downloaded earlier.
   
   - Password: Enter your Secret access key from the IAM User credentials you downloaded earlier.
   
   - Once you've entered these values, select Save and Add Another.
    
5. On the next create connection page, enter the following values:

   - Conn Id: Enter redshift.
   - Conn Type: Enter Postgres.
   - Host: Enter the endpoint of your Redshift cluster, excluding the port at the end. You can find this by selecting your cluster in the Clusters page of the Amazon    - Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to NOT include the port at the end of the Redshift endpoint string.
   - Schema: Enter dev. This is the Redshift database you want to connect to.
   - Login: Enter awsuser.
   - Password: Enter the password you created when launching your Redshift cluster.
   - Port: Enter 5439.
   - Once you've entered these values, select Save.


6. Awesome! You're now all configured to run Airflow with Redshift.

** WARNING: Remember to DELETE your cluster each time you are finished working to avoid large, unexpected costs. **


