# Install Airflow on Ubuntu via Pip
> Adapted from: https://www.geeksforgeeks.org/how-to-install-apache-airflow/

### 1. Define a directory for **Airflow Home**
- In `~/.bashrc`
  - `export AIRFLOW_HOME=$HOME/local/airflow`
  NB: you can define your own Airflow home directory

### 2. Install Apache Airflow using pip
- `pip install apache-airflow`

  NB: you can install a virtual environment before.

### 3. Install Apache Airflow Amazon Providers
- `pip install apache-airflow-providers-amazon`
  NB: This enables connection options between Airflow and AWS

### 4. Backend initialization to maintain workflow
- `airflow db init`

### 5. Configure Airflow (DAG folder, Plugin folder, ...)
- In order to **_our_ DAGs** and **Plugins** _work properly_, we need to inform Airflow _which are the folders_ where our codes are.
- To do this, open the `airflow.cfg` file inside the _Airflow installation folder_ (in my case, `$HOME/local/airflow`).
    - Change the `dag_folder`:
      - `dags_folder = <your_project_root_folder>/dags`
    - Change the `plugins_folder`:
      - `plugins_folder = <your_project_root_folder>/plugins`

    Any _python code_ _inside_ these folders (or in subfolders) will be _automatically recognized_ by **Airflow UI**.


### 6. Create a user and password to access Airflow UI
- `airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin`
  NB: In this case, my _username_ and _password_ are `admin`

### 7. Start the web server / Apache user interface
- `airflow webserver -p 8080`

### 8. Airflow scheduler to monitor workflow
- `airflow scheduler`
- The DAG list won't be refreshed without this

### 9. Open Airflow UI on your browser
- `localhost:8080`

### 10. Test a DAG
- I left a _hello world DAG_ in `./dags/greet_flow_dag.py`
- On Airflow UI in the DAG list, check the DAG called `greet_flow_dag`
- By enabling it, it will be performed according to its schedule
- To execute immediately, click on the `play` button > Trigger DAG
- The circles in front of the DAG name in the DAG list shows the runs and their status
- We can inspect the runs and other properties (such as its Graph) by clicking on the DAG name
- Click on Graph tab
  - The single `hello_world_task` block will be green (indicating a success)
  - Click on the block > Log and see the printed message by our code
    - .... {greet_flow_dag.py:15} INFO - Hello World!


### 11. Important Notes
#### **Airflow directories in `PYTHONPATH`
The pathnames defined in `airflow.cfg` for our **DAGs** and **plugins** folders are automatically added to `PYTHONPATH` when importing **Airflow** package. We can see this configuration by running `airflow info` on the terminal. See the `python_path` output.

However, the inclusion of these Airflow folders _only_ happens when **importing Airflow**. Let's test it.

Open the _python interactive terminal_ and type:
```
import sys
print(sys.path)
```

Note that the _output_ of the `PYTHONPATH` (`sys.path`) does not include any Airflow directory. But, if we _import airflow_ and run the same code again:
```
import airflow

import sys
print(sys.path)
```

```
Out[1]: 
[...,
 '<PROJECT_FULL_DIRECTORY>/project-airflow-aws/dags',
 '<PROJECT_FULL_DIRECTORY>/project-airflow-aws/plugins']
```

Now we can see the **DAG** and **Plugins* folders in the `PYTHONPATH` (`sys.path`). Consequently, we can import _python packages and modules_ that are inside these directories. For example, the _plugins folders_ of my project has these files:
```
project-airflow-aws
│ ...
├── plugins
│   ├── operators
│   │   ├── __init__.py
│   │   ├── stage_redshift.py
│   │   └── ...
└── ...
```

The `operators` folder inside `plugins` is a python package since it contains a `__init__.py` file. We could then do something like this:
```
# import the operators package
import operators

# import a specific module
from operators import stage_redshift
```
We refer to this [link](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/modules_management.html) for more details.


#### **Problems when automatically loading modified scripts in Airflow**
During the project development, **sometimes Airflow did not recognized changes in some python files**, especially non-dag files (for example, those inside the _plugins_ folder). The simplest solution is **to kill and relaunch the webserver and scheduler**.
