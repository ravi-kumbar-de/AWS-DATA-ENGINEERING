CREATE EXTERNAL TABLE IF NOT EXISTS `step_trainer_landing`(
  `sensorreadingtime` bigint, 
  `serialnumber` string, 
  `distancefromobject` int
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe' 
WITH SERDEPROPERTIES ( 
  'case.insensitive' = 'TRUE', 
  'dots.in.keys' = 'FALSE', 
  'ignore.malformed.json' = 'FALSE', 
  'mapping' = 'TRUE'
) 
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://stedi-lake-house-samucoding/step_trainer/landing'
TBLPROPERTIES ('classification'='json', 'transient_lastDdlTime'='1690332095')