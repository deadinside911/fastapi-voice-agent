"""
Test the webhooks
"""
from services.webhook_services import WebhookServices


def test_transcripts(client):
    message = "hello"

    header_name = WebhookServices.signature_header
    request_header = WebhookServices.create_signature(message)

    response = client.post(
        "/webhooks/transcripts",
        params={
            "message": message,
        },
        headers={header_name: request_header},
    )

    assert response.status_code == 200

    # Tampered message
    response = client.post(
        "/webhooks/transcripts",
        params={
            "message": message + " ",
        },
        headers={header_name: request_header},
    )

    assert response.status_code == 403
