import boto3 # type: ignore
from PIL import Image
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'file-conversion-bucket'

    # Get the file details from the S3 event
    key = event['Records'][0]['s3']['object']['key']
    response = s3.get_object(Bucket=bucket_name, Key=key)
    file_content = response['Body'].read()

    # Convert the file to PNG
    img = Image.open(io.BytesIO(file_content))
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)

    # Save the converted file in the output folder
    new_key = key.replace('input/', 'output/').replace('.jpg', '.png')
    s3.put_object(Bucket=bucket_name, Key=new_key, Body=output)
    return {
        'statusCode': 200,
        'body': f'File converted and saved to {new_key}'
    }
