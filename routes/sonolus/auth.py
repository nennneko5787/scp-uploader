import base64
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicNumbers
from fastapi import APIRouter, Header, HTTPException, Request, Response

from objects import ServerAuthenticateRequest, ServerAuthenticateResponse

router = APIRouter()

JWK_PUBLIC_KEY = {
    "kty": "EC",
    "crv": "P-256",
    "x": "d2B14ZAn-zDsqY42rHofst8rw3XB90-a5lT80NFdXo0",
    "y": "Hxzi9DHrlJ4CVSJVRnydxFWBZAgkFxZXbyxPSa8SJQw",
}


def b64urlDecode(data: str) -> bytes:
    data += "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data)


# 公開鍵を構築
def getPublicKeyFromJwk(jwk: dict):
    x_bytes = b64urlDecode(jwk["x"])
    y_bytes = b64urlDecode(jwk["y"])
    x = int.from_bytes(x_bytes, "big")
    y = int.from_bytes(y_bytes, "big")
    public_numbers = EllipticCurvePublicNumbers(x, y, ec.SECP256R1())
    return public_numbers.public_key(default_backend())


@router.post("/sonolus/authenticate")
async def sonolusAuth(
    request: Request,
    response: Response,
    model: ServerAuthenticateRequest,
    signature: str = Header(alias="sonolus-signature"),
) -> ServerAuthenticateResponse:
    response.headers.update({"Sonolus-Version": "1.0.0"})

    try:
        signatureBytes = base64.b64decode(signature)
    except Exception:
        raise HTTPException(400, detail="Invalid base64 in sonolus-signature header")

    body = await request.body()

    publicKey = getPublicKeyFromJwk(JWK_PUBLIC_KEY)

    try:
        publicKey.verify(signatureBytes, body, ec.ECDSA(hashes.SHA256()))
    except InvalidSignature:
        raise HTTPException(401, detail="Signature verification failed")

    # verified
    now = time.time()

    # 時間の差を求め、ガチでズレズレだったら弾く
    if abs(now - (model.time / 100)) > 20:
        raise HTTPException(400, detail="Your watch is too bad...")

    # あとはredisに値ぶち込むとか。。。？

    return ServerAuthenticateResponse(
        session="<ここにセッショントークンを入力>", expiration=(now + (60 * 20) * 100)
    )
