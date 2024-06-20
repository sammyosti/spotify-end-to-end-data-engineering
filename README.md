# Spotify End-To-End Data Engineering Project: Extract, Transform, and Analyze with AWS.
# Introduction
<div align="justify">This project aims to create a seamless and efficient data pipeline for Spotify data using AWS services. The goal is to fetch, transform, and analyze Spotify data in an organized and easily accessible manner. Here’s how it will be done:</div>

### Step 1: Data Extraction with AWS Lambda
<div align="justify">First, the pipeline will connect to the Spotify API to pull in relevant data. To automate this process, the code will be deployed on AWS Lambda. This setup will run at scheduled intervals or trigger events, ensuring the consistent gathering of the latest data without manual intervention.</div>

### Step 2: Transforming the Data
<div align="justify">Once the data is acquired, the next step is to clean and format it. The transformation function will handle tasks like normalizing data, aggregating information, and filtering based on specific needs. This ensures that the data is ready for detailed analysis.</div>

### Step 3: Automating the Transformation Process
<div align="justify">To maintain efficiency and reliability, an automated trigger will be built on top of the transformation function. This trigger will monitor for any updates in the extracted data and execute the transformation process as needed.</div>

### Step 4: Storing the Transformed Data
<div align="justify">After transforming the data, it will be stored back in AWS S3, maintaining a well-organized file structure. This organization makes it easy to retrieve and use the processed data for further analysis.</div>

### Step 5: Enabling Seamless Analytics
<div align="justify">For the final step, analytics tables will be set up using AWS Glue and Athena. These services will help define the data schema and enable efficient querying and analysis of the transformed data. This setup will unlock valuable insights from the Spotify data.</div>

# Architecture
![spotify](https://github.com/sammyosti/spotify-end-to-end-data-engineering/assets/78179187/f498adb0-775b-4427-98bb-18aa5912d397)

### Services Used: 
* **Spotify API:** The Spotify API provides developers with access to Spotify's vast music catalog and user data, allowing them to integrate Spotify’s features into their applications. It supports operations like searching for music, retrieving playlists, and accessing user profile information. - [Spotify API](https://developer.spotify.com/documentation/web-api/).
* **Amazon CloudWatch:** Amazon CloudWatch is a monitoring and observability service designed to provide actionable insights into your AWS resources and applications. It collects and tracks metrics, collects and monitors log files, sets alarms, and automatically reacts to changes in your AWS environment to ensure operational health and performance.
* **AWS Lambda:** AWS Lambda is a serverless compute service that runs code in response to events and automatically manages the underlying compute resources. It allows developers to execute code without provisioning or managing servers, simplifying the development of scalable and responsive applications.
* **AWS S3 (Simple Storage Service):** Amazon S3 is a scalable object storage service designed for storing and retrieving any amount of data from anywhere on the web. It provides robust data durability, security, and cost-effective storage options for a wide range of use cases, including backups, content distribution, and big data analytics.
* **AWS Glue Crawler:** AWS Glue Crawler is a tool that automatically scans your data sources, identifies data formats, and populates the AWS Glue Data Catalog with the corresponding table definitions. It simplifies the process of data discovery and cataloging by automating the detection of schema changes and updates.
* **AWS Glue Data Catalog:** The AWS Glue Data Catalog is a centralized metadata repository that stores information about data stored across various data sources, such as Amazon S3 and relational databases. It enables seamless integration and easy access to data for ETL processes and analytics, supporting schema versioning and fine-grained access control.
* **Amazon Athena:** Amazon Athena is an interactive query service that makes it easy to analyze data directly in Amazon S3 using standard SQL. It is serverless, so there is no infrastructure to manage, and users only pay for the queries they run, making it a cost-effective solution for big data analysis.

### To install packages:
```
pip install pandas
pip install spotipy
pip install numpy
```





