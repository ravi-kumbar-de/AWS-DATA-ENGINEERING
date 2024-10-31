# Project: Data Modeling with Apache Cassandra

<img src='./imgs/audio_wallpaper_cassandra.png' style='width: 100%' />

> **Note:** This project is part of [Data Engineering with AWS nanodegree program](https://www.udacity.com/course/data-engineer-nanodegree--nd027).


## 1. Project Description
A startup called _Sparkify_ wants to analyze the data they've been collecting on _songs and user activity_ on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a **directory of CSV files** on user activity on the app.

They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring you on the project. Your role is to create a database for this analysis. You'll be able to test your database by running queries given to you by the analytics team from Sparkify to create the results.

### 🎯 Goal
Create an **Apacha Cassandra database**  which can perform _queries_ on song play data for analysis.

## 2. Project Structure
```
project-apache-cassandra
├── event_data                                    # directory with the data
│   └── ...
├── event_datafile_new.csv                        # dataset to create denormalized data
└── project_apache_cassandra_data_modeling.ipynb  # proposed solution

```

## 3. Project datasets
For this project, you'll be working with **one dataset**: `event_data`. The **directory of CSV files** is partitioned by _date_. Here are examples of filepaths to two files in the dataset:

```
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
```

## 4. Proposed Solution
The proposed solution can be found on `./project_apache_cassandra_data_modeling.ipynb` notebook.

The solution consists of the following steps:
1. Iterate through each event file in event_data **to process and create** a new CSV file in Python
2. Include Apache Cassandra `CREATE` and `INSERT` statements **to load processed records** into relevant tables in your data model
3. Test by running `SELECT` statements after running the queries on your database
