# belong-data-challenge

***Requirements:***

  python3

  pip3 install -r requirements.txt

***Run***
  
  python3 <path>/belong-data-challenge/ped_data.py
  
  Produces results locally daily_ped_count_results.csv and monthly_ped_count_results.csv and also under the s3 bucket: 
    https://s3.console.aws.amazon.com/s3/buckets/firstpractise?region=ap-southeast-2&tab=objects

  Note: Code uses AWS S3 access/secret key which is in the code, this would be removed after sometime. The read access on the S3 bucket is public.
  
  
***Architecture:*** 

  This solution uses Pandas Dataframes to read  the Melbourne Pedestrain Data API 1000000 rows at once and create a locally stored csv file: resources/ped_source.csv.

  It uses the Pandas groupby, and applies custom aggregate or lambda to find sum hourly_counts grouped based on year,month,mdate, sensor_id. 

  Then we pick the top 10 results 
    1. Per day but grouped and summed using sensor_id, year,month, mdate
    2. Per month grouped and summed using sensor_id, year,month

  We store the above calculated values in daily_ped_count_results.csv and monthly_ped_count_results.csv locally. We also write to S3 object store this is just result files, but with enough time we could make the program write date wise folders with respective results files in those folders and then write to AWS RedShift
  
  
  TBD
 Data in S3 can copied over to RedShift cluster, this is a much faster approach and can be done via the same python code, (much faster compared to writing pandas.to_sql(redshifturl, dataframe)...)as this considerably slows down when the in memory size of the PD dataframe is larger than say 100MB.
 
 Store data in AWS RedShift cluster so that the data can be partitioned on date basis and month basis and further analysed using SQL or RedShift APIs. This allows not querying the entire dataset but rather just the partitions.
  
Also can be stored is the Sensor related metdata in RedShift cluster as a separate table for eg: to allow cross SQL queyring of datasets and merge data to allow to see which Sensor ID matches which Address and the likes. 
  **This could futher be improved by adding geolocation data using the address so that a map view of highest counts is possible**

***Performance***
  
 The code runs in less than few seconds for a 1Million row dataframe queried however when larger (GBs) CSV files have to be processed it would be best to chunk and read the files and create Datewise batched csv files to reduce memory burden on the resources. 

***Tests***

Basic tests in test/test_ped_data.py runs and checks if the result files are created...




