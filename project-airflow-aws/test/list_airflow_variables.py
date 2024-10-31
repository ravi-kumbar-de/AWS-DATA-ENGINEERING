from airflow.models import Variable

print(Variable.get('region'))
print(Variable.get('s3_bucket'))
print(Variable.get('s3_prefix_log_data'))
print(Variable.get('s3_prefix_log_json_path'))
print(Variable.get('s3_prefix_song_data'))
