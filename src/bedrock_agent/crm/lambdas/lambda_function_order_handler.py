import json
import logging

import boto3
import os
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)


s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'inline-agent-sample-orders-bucket')


def lambda_handler(event, context):
    logger.info(f"Calling function with API path: {event['apiPath']}")
    logger.info(f"Calling function from Action Group: {event['actionGroup']}")

    method = event.get("httpMethod")
    path_params = event.get("pathParameters") or {}
    order_id = path_params.get("id")
    if not order_id:
        parameters = event.get("parameters", [])
        order_id = next((param['value'] for param in parameters if param['name'] == 'id'), None)

    try:
        if method == "POST":
            logger.info(f"Creating order")
            return create_order(event)
        elif method == "GET" and order_id:
            logger.info(f"Getting order: {order_id}")
            return get_order(order_id, event)
        elif method == "PUT" and order_id:
            logger.info(f"Updating order: {order_id}")
            return update_order(order_id, event)
        elif method == "DELETE" and order_id:
            logger.info(f"Deleting order: {order_id}")
            return delete_order(order_id, event)
        else:
            if not order_id and method != "POST":
                logger.info(f"Missing order ID")
                return response(400, {"error": "Missing order ID"}, event)
            logger.info(f"Unsupported method: {method}")
            return response(400, {"error": "Unsupported method or missing order ID"}, event)
    except Exception as e:
        return response(500, {"error": str(e)}, event)


def normalize_bedrock_event(event):
    """Parses Bedrock agent-style payload into a proper JSON dict."""
    logger.info(f"Normalizing Bedrock event: {event}")
    props = event["requestBody"]["content"]["application/json"]["properties"]
    logger.info(f"Properties: {props}")
    payload = {prop["name"]: prop["value"] for prop in props}
    logger.info(f"Payload: {payload}")

    # Normalize numeric values
    if "total" in payload:
        payload["total"] = float(payload["total"])

    # Normalize nested orderLines if needed
    raw_order_lines = payload.get("orderLines")
    logger.info(f"Raw order lines: {raw_order_lines}")
    if isinstance(raw_order_lines, str):
        logger.info(f"Raw order lines is a string: {raw_order_lines}")

        pattern = r"{(?:item|product)=([^,]+), quantity=(\d+)}"
        matches = re.findall(pattern, raw_order_lines)
        payload["orderLines"] = [
            {"product": item.strip(), "qty": int(qty)}
            for item, qty in matches
        ]
    logger.info(f"Payload: {payload}")

    return payload

def create_order(event):
    logger.info(f"In the create_order method with event {event}")

    # Determine if this is a Bedrock invocation
    if "requestBody" in event:
        body = normalize_bedrock_event(event)
    else:
        body = json.loads(event["body"])

    logger.info(f"Parsed body: {body}")
    order_id = body.get("orderId")
    if not order_id:
        logger.info("Missing orderId in body")
        return response(400, {"error": "Missing orderId in body"}, event)

    key = f"orders/{order_id}.json"
    logger.info(f"Creating order: {order_id} and body {json.dumps(body)}")
    try:
        # Check if the order already exists
        s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=json.dumps(body))
    except Exception as e:
        logger.info(f"Error creating order: {e}")
        return response(500, {"error": str(e)}, event)

    logger.info(f"Order created: {order_id} and stored in the S3 Bucket")
    return response(200, {"confirmationMessage": "Order created", "orderId": order_id}, event)

def get_order(order_id, event):
    key = f"orders/{order_id}.json"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        order_data = json.loads(obj["Body"].read().decode("utf-8"))
        return response(200, order_data, event)
    except s3.exceptions.NoSuchKey:
        return response(404, {"error": "Order not found"}, event)


def update_order(order_id, event):
    body = json.loads(event["body"])
    key = f"orders/{order_id}.json"
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=json.dumps(body))
    return response(200, {"message": "Order updated", "order_id": order_id}, event)


def delete_order(order_id, event):
    key = f"orders/{order_id}.json"
    s3.delete_object(Bucket=BUCKET_NAME, Key=key)
    return response(204, None, event)


def response(status_code, body, event):
    return {
        "response": {
            "actionGroup": event['actionGroup'],
            "apiPath": event['apiPath'],
            "httpMethod": event.get("httpMethod", "POST"),
            "httpStatusCode": status_code,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body) if body else None
                }
            }
        }
    }