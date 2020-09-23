# Prerequisites

You need the following dependencies to run this job:

## S3 Credentials Secret

You need a secret in the **spark** namespace called **s3-credentials** that defines the following keys:
- spark.hadoop.fs.s3a.access.key 
- spark.hadoop.fs.s3a.secret.key

The secret should be declared using spark's configuration file format with the **=** chracter separating the keys from the values as opposed to the **:** character.

## Test Jar Accessible with S3

You should have a test jar in your ceph cluster that you can use to run the ceph test.

From there, you can override the **SPARK_CLASS** and **SPARK_JAR** variable names in the spark job.

For example, if you have jar named **test-ceph.jar** in the **spark** bucket with a **bio.ferlab.clin.etl.TestCeph** entrypoint class, the **SPARK_CLASS** environment variable would have a value of **bio.ferlab.clin.etl.TestCeph** and the **SPARK_JAR** environment variable would have a value of **s3a://spark/test-ceph.jar**.

# A Ceph Endpoint Override

The **spark-ceph-endpoint** config map should be overidden so that the **spark.hadoop.fs.s3a.endpoint** key is set to your ceph endpoint.

For example, if you are using Calcul Quebec, it would look like this:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: spark-ceph-endpoint
  namespace: spark
  labels:
    name: spark
data:
  spark-ceph-endpoint.conf: |
    spark.hadoop.fs.s3a.endpoint=https://esc.calculquebec.ca:8080
```
