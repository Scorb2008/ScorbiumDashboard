import hashlib
import hmac

from app.services.webhook_security import compute_cryptobot_hmac, verify_cryptobot_signature


def test_compute_cryptobot_hmac_uses_raw_json_body():
    token = "12345:secret-token"
    raw_body = b'{"update_type":"invoice_paid","payload":{"invoice_id":1}}'

    expected = hmac.new(
        hashlib.sha256(token.encode()).digest(),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    assert compute_cryptobot_hmac(token, raw_body) == expected


def test_verify_cryptobot_signature_rejects_modified_body():
    token = "12345:secret-token"
    raw_body = b'{"update_type":"invoice_paid","payload":{"invoice_id":1}}'
    signature = compute_cryptobot_hmac(token, raw_body)

    assert verify_cryptobot_signature(raw_body, signature, token) is True
    assert (
        verify_cryptobot_signature(
            b'{"update_type":"invoice_paid","payload":{"invoice_id":2}}',
            signature,
            token,
        )
        is False
    )
