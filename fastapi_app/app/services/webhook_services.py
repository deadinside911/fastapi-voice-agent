"""
Webhook services
"""
import hashlib
import hmac
import os

WEBHOOK_SECRET_KEY = os.getenv("WEBHOOK_SECRET_KEY", "webhook-secret-key").encode(
    "utf-8"
)


class WebhookServices:
    """
    Creates and validates header signature
    """

    signature_header = "X-QA-Signature"

    @staticmethod
    def create_signature(message: str):
        """ """
        signature = hmac.new(
            key=WEBHOOK_SECRET_KEY,
            msg=message.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return signature

    @staticmethod
    def validate_signature(message: str, signature: str):
        """ """
        return hmac.compare_digest(signature, WebhookServices.create_signature(message))
