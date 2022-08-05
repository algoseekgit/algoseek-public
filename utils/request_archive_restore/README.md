# Request Archive Restore


## Introduction

This script is used to submit a job to restore and copy S3 objects from Glacier or Glacier Deep Archive storage
into your own S3 bucket. 

In order to get started you need to request algoseek-provisioned AWS credentials used to invoke the script.
Please submit a support ticket to support@algoseek.com with your order number included.

The following sections discuss in detail the command-line arguments and sample usage.

## Command-Line Arguments


Positional arguments:

| Name           | Description                                                             |
| -------------- | ----------------------------------------------------------------------- |
|  manifest      | A path to a csv file with a comma-separated list of bucket names and object paths (or path prefixes) to restore |


Keyword arguments:

| Name             | Description                                                 |
| ---------------- | ----------------------------------------------------------- |
|  --manifest_mode | If `prefixes` mode is used the second column in the manifest file is treated as object path prefix rather than a full path (default: full_path) |
|  --dest_bucket   | A name of the S3 bucket to which objects should be copied when restored (required) |
|  --email         | An email address for status notofications (Skip if you do not need status notifications)  |
|  --profile       | AWS profile name (default: use default credentials) |


### Manifest structure

A manifest is a CSV file with two columns: bucket name and object path (prefix).
The format of the second column is specified with `manifest_mode` argument which can be either `full_path` or `prefixes`.

#### Path prefixes mode

When `manifest_mode` is set to `prefixes` the manifest is interpreted as a list of path prefixes, so all objects with the file prefix you have provided will be restored.

Example manifest file with path prefixes:
```
us-options-tanq-2020,20201231/P/PDD/
us-options-tanq-2020,20201231/I/INTC/
us-options-tanq-2020,20201231/S/SMH/
us-options-tanq-2020,20201231/G/GLD/
us-options-tanq-2020,20201231/L/LULU/
us-options-tanq-2020,20201231/X/XRT/

```
It means, for example, that all files under `20201231/P/PDD/` prefix will be restored:
```
PDD.20201231.tar
PDD.20210108.tar
PDD.20210115.tar
PDD.20210122.tar
PDD.20210129.tar
PDD.20210205.tar
PDD.20210212.tar
PDD.20210219.tar
PDD.20210416.tar
PDD.20210618.tar
PDD.20210716.tar
PDD.20220121.tar
PDD.20230120.tar
```

Use this option when you need all option chains for a base symbol or the whole trading day.

To restore one day of data (e.g. Dec 31, 2020) use the following prefix format
```
us-options-tanq-2020,20201231
```

#### Full path mode

If you intend to restore individual files (option chains), you can make use of the `full_path` manifest mode.
It indicates that the second column in your manifest file corresponds to a single object in S3.

Example manifest file with path prefixes:
```
us-options-tanq-2020,20201231/P/PDD/PDD.20201231.tar
us-options-tanq-2020,20201231/P/PDD/PDD.20210205.tar
us-options-tanq-2020,20201231/P/PDD/PDD.20210716.tar
```

You can include multiple source buckets in your manifest file:
```
us-options-tanq-2015,20151202/P/PDD/
us-options-tanq-2019,20190913/P/PG/
us-options-tanq-2020,20201231/P/PDD/
```

You cannot mix path prefixes and full object paths in a single manifest file.

If you do need both prefixes and full paths to be restored please submit these as two separate jobs. 

### Bucket access

Please make sure your `dest_bucket` gives the write access to the algoseek service role which will copy the rewtored objects to the bucket.
A sample bucket policy is provided below:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "algoseek-write-only-restored-objects",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::545933605308:role/AWSBatchServiceRole"
            },
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::BUCKET-NAME/*"
        }
    ]
}
```
Make sure to replace `BUCKET-NAME` in the policy with your actual bucket name.

### Email notifications

We do suggest to enable email notifications with `--email your-email@example.com`, 
so you could track status changes and recieve any error messages if something goes wrong.

## Usage


Restore objects listed in `manifest.csv` to `my-bucket-name` S3 bucket.

```
python3 submit_restore_request.py manifest.csv --dest_bucket my-bucket-name
```

Restore objects listed in `manifest.csv` to `my-bucket-name` S3 bucket with email notifications to `jdoe@example.com`
using a named AWS profile `algoseekdata`. 

```
python3 submit_restore_request.py manifest.csv --dest_bucket my-bucket-name --email jdoe@example.com --profile algoseekdata
```


## Limitations

It takes about 48 hours to restore and copy an object from archive.

You can submit up to 60 000 objects per invocation. Note, if you a providing path prefixes in your manifest file, the 
object count will be based on the prefix expansion to the list of full paths.
For example, if you submit 20 000 prefixes and each leading to 5 paths, your final manifest file would have 5 x 20 000 = 100 000 objects and will be rejected.

The script only works with archived S3 objects. If you provide objects from the Standard storage class they won't be proecced.
To copy standard objects use `aws cli` or `boto3` python library.


