import boto3

client = boto3.client("bedrock", region_name="us-east-1")

try:
    response = client.list_foundation_models()
    print("Bedrock access OK")
    print(len(response["modelSummaries"]))
except Exception as e:
    print("Error:", e)