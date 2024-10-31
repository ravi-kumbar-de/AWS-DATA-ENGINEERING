# Connecting Redshift cluster with SQL Workbench/J on Linux Mint
My notes about how to connect a _Redshift cluster_ using **SQL Workbench/J**. <br/>
References:
- https://www.youtube.com/watch?v=iLBTq-2DKPk
- https://docs.aws.amazon.com/redshift/latest/mgmt/connecting-using-workbench.html

## 1. Installing SQL Workbench/J
- SQL Workbench/J requires Java 11 or later. Using Java 17 is recommended.
- Go to the [download page](https://www.sql-workbench.eu/downloads.html)
- Click on _Generic package for all systems including all optional libraries_.
- Download the file in the installation folder of your choice
- Unzip it
- If you need to install JRE
  - On terminal, go to the _installation folder_
  - `./download_jre.sh`
- To **run _SQL Workbench/J_**
  - On terminal, go to the _installation folder_
  - `./sqlworkbench.sh`
- To add it in the Linux Mint menu
  - Open the menu (super key)
  - Type _Main menu_
  - Add a new item for the `sqlworkbench.sh`

## 2. Download the Amazon Redshift JDBC driver
- On [the official documentation](https://docs.aws.amazon.com/redshift/latest/mgmt/connecting-using-workbench.html)
  - Click on _Download the Amazon Redshift JDBC driver_
  - Download the file on the `<sql_workbench_installation_folder>/ext/JDBCDrivers/`
  - Unzip the file

## 3. Connecting Redshift cluster with SQL Workbench/J
- Open _SQL Workbench/J_
- File > Connect window
  - An open to _select a connection profile_ will open
- Give a name for your profile
- Click on the `Manage Drivers` button
  - Create a new entry/driver (by clicking on the new button)
  - **Name:** _AWS Redshift JDBC Driver_
  - On **Library**, click on the folder button (_Select the Jars.._)
  - Select all **Redshift JDBC connector _jar files_** donwload in Step 2.
    - In my case, there were 4 files
  - On a popup, select the _redishift_ dirve: `com.amazon.redshift.Driver`
    - This name will be assigned to _Classname_
  - In **Sample URL**:
    - Paste the your _Cluster JDBC URL_
    - You can find this URL on your _Redshift cluster dashboard_ on _AWS Redshift_.
- **Driver**: Select _AWS Redshift JDBC Driver_
- **Username**: your database username found in `dwh.cfg` file
- **Password**: your database password found in `dwh.cfg` file
- Other options selected:
  - Autocommit
  - Confirm updates
  - Save passwords
  - Include NULL columns in INSERTS
- Click ok to connect to your Redshift Cluster Database

Now, we can see the _Database Tree_, _Database Explorer_, and run _SQL statements_.