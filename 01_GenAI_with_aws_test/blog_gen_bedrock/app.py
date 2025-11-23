import os
import json
import boto3
import botocore.config
from botocore.exceptions import ClientError

from datetime import datetime

REGION = "eu-west-1"

def blog_generate_using_bedrock(blogtopic:str,
                                model_id:str = "eu.meta.llama3-2-3b-instruct-v1:0")-> str:
    
    prompt = f"Write a 200-word blog post on the topic: {blogtopic}"

    formatted_prompt = f"""
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>
    {prompt}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    native_request ={
        "prompt": formatted_prompt,
        "temperature": 0.5,
        "top_p": 0.9,
        "max_gen_len": 512
    }

    try:
        # Create a Bedrock Runtime client
        bedrock_client = boto3.client("bedrock-runtime",
                                      region_name=REGION,
                                      config=botocore.config.Config(read_timeout=300,
                                                                    retries={'max_attempts':3}))
        
        # Convert the native request to JSON
        request = json.dumps(native_request)
        
         # Invoke the model with the request.
        response = bedrock_client.invoke_model(body=request,
                                               modelId=model_id)

        # Decode the response body
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        print(response_data)
        
        # Extract and print the response text.
        blog_details = response_data['generation']
        return blog_details
    
    except Exception as e:
        print(f"Error generating the blog:{e}")
        return ""

def create_s3_bucket(bucket_name: str, region: str = REGION):
    s3_client = boto3.client('s3', region_name=region)
    try:
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists and is owned by you.")
            return True
        elif error_code == 'BucketAlreadyExists':
            print(f"Bucket '{bucket_name}' already exists and is owned by someone else.")
            return False
        else:
            print(f"Error creating bucket: {e}")
            return False
    return True


def save_blog_details_s3(s3_key, s3_bucket, generate_blog, region = REGION):
    # Ensure bucket exists (create if not)
    if not create_s3_bucket(s3_bucket, region):
        print("Cannot proceed without a valid bucket.")
        return ""
    
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog )
        print("Code saved to s3")
        return True
    except Exception as e:
        print(f"Error when saving the code to s3: {e}")
        return False


def lambda_handler(event, context):
    try:
        event = json.loads(event['body'])
        blogtopic = event['blog_topic']

        generate_blog = blog_generate_using_bedrock(blogtopic=blogtopic)

        if generate_blog:
            current_time = datetime.now().strftime('%H%M%S')
            s3_key = f"blog-output/{current_time}.txt"
            s3_bucket = "boto3-bedrock-genai-project" #os.environ['S3_BUCKET_NAME']
            success = save_blog_details_s3(s3_key, s3_bucket, generate_blog, region=REGION)
            if not success:
                return {
                    'statusCode': 500,
                    'body': json.dumps('Failed to save blog to S3')
            }
            
        else:
            print("No blog was generated")
            return {
                'statusCode': 400,
                'body': json.dumps('Blog generation failed')
            }

        return {
            'statusCode': 200,
            'body': json.dumps('Blog generation completed successfully')
        }
    except Exception as e:
        print(f"Lambda error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal error: {str(e)}')
        }