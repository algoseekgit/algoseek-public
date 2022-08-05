# Copyright 2021 AlgoSeek, LLC. All Rights Reserved

import json
import uuid
import pathlib
import argparse
import datetime

import boto3


def setup_parser():
    parser = argparse.ArgumentParser(
        description='Restore and copy S3 objects from Glacier or Glacier Deep Archive storage'
    )
    parser.add_argument(
        'manifest', type=pathlib.Path,
        help='A path to the csv file with a comma-separated list of bucket names and object paths (or path prefixes) to restore'
    )
    parser.add_argument(
    	'--manifest_mode', choices=['prefixes', 'full_path'], default='full_path',
    	help = 'If `prefixes` mode is used the second column in the manifest file is treated as object path prefix rather than a full path (default: %(default)s)'
    )
    parser.add_argument(
    	'--dest_bucket',
    	required=True,
    	help='A name of the S3 bucket to which objects should be copied when restored'
    )
    parser.add_argument(
        '--email',
        help='An email address for status notofications'
    )
    parser.add_argument(
        '--profile', default='default',
        help='AWS profile name (default: %(default)s)'
    )
    return parser


def copy_manifest_to_s3(s3, bucket_name, manifest_file_path, payload):
    try:
        s3.Object(
            bucket_name,
            payload['manifest_obj_key']
        ).upload_file(manifest_file_path)
        s3.Object(
            bucket_name,
            payload['config_obj_key']
        ).put(Body=(json.dumps(payload).encode('UTF-8')))
    except Exception as e:
        print(f'Failed to upload the manifest file: {e}')


def invoke_step_machine(client, state_machine_arn, job_id, payload):
    try:
        response = client.start_execution(
            stateMachineArn=state_machine_arn,
            name=job_id,
            input=json.dumps(payload)
        )
    except Exception as e:
        print(f'Failed to start the restore job: {e}')


###########################################################


if __name__ == '__main__':
    parser = setup_parser()
    args = parser.parse_args()

    config_bucket_name = 'as-gda-restore-objects-details'
    step_machine_arn = 'arn:aws:states:us-east-1:545933605308:stateMachine:as-gda-restore-objects'

    session = boto3.Session(profile_name=args.profile)

    s3 = session.resource('s3')
    sts = session.client('sts') 
    client = session.client('stepfunctions', region_name='us-east-1')

    today = datetime.date.today()
    uid = str(uuid.uuid4()).split('-')[0]
    user_name = sts.get_caller_identity().get('Arn').split('/')[-1]
    
    job_id = f'{user_name}-{today}-{uid}'
    object_prefix = f'{user_name}/{today.year}/{today.month}/{today.day}{uid}'
    
    payload = {
        "logs_bucket_name": config_bucket_name,
        "logs_prefix": object_prefix,
        "manifest_obj_key": f"{object_prefix}/manifest.csv",
        "config_obj_key": f"{object_prefix}/config.json",
        "manifest_mode": args.manifest_mode,
        "job_id": job_id,
        "user_name": user_name,
        "email": args.email,
        "dest_bucket": args.dest_bucket        
    }
    copy_manifest_to_s3(s3, config_bucket_name, str(args.manifest), payload)
    invoke_step_machine(client, step_machine_arn, job_id, payload)
    print(f'The restore job was successfully submitted. Your job id is {job_id}')
    if args.email:
        print(f"We will send email notofications to {args.email} when the job status shanges")
