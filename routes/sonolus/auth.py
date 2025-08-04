import base64
import secrets
import string
from datetime import datetime, timedelta, timezone

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicNumbers
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from fastapi import APIRouter, Header, HTTPException, Request, Response

from objects import ServerAuthenticateRequest, ServerAuthenticateResponse
from services.db import DBService

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


def getPublicKeyFromJwk(jwk: dict):
    x_bytes = b64urlDecode(jwk["x"])
    y_bytes = b64urlDecode(jwk["y"])
    x = int.from_bytes(x_bytes, "big")
    y = int.from_bytes(y_bytes, "big")
    public_numbers = EllipticCurvePublicNumbers(x, y, ec.SECP256R1())
    return public_numbers.public_key(default_backend())


def randomAuthCode(n: int):
    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(n)
    )


@router.post("/sonolus/authenticate")
async def sonolusAuth(
    request: Request,
    response: Response,
    model: ServerAuthenticateRequest,
    signature: str = Header(alias="sonolus-signature"),
) -> ServerAuthenticateResponse:
    response.headers.update({"Sonolus-Version": "1.0.0"})

    # Sonolus-Signature ヘッダの base64url decode
    try:
        signatureBytes = b64urlDecode(signature)
    except Exception:
        raise HTTPException(400, detail="Invalid base64url in sonolus-signature header")

    # raw形式（r||s 64バイト）→ DER変換
    if len(signatureBytes) == 64:
        r = int.from_bytes(signatureBytes[:32], "big")
        s = int.from_bytes(signatureBytes[32:], "big")
        signatureBytes = encode_dss_signature(r, s)

    # リクエストボディ取得（クライアントの署名対象と一致する必要あり）
    body = await request.body()

    # 公開鍵構築
    publicKey = getPublicKeyFromJwk(JWK_PUBLIC_KEY)

    # 署名検証
    try:
        publicKey.verify(signatureBytes, body, ec.ECDSA(hashes.SHA256()))
    except InvalidSignature:
        raise HTTPException(401, detail="Signature verification failed")

    now = datetime.now(timezone(timedelta(hours=9), "Asia/Tokyo")).timestamp()

    # 時計のズレチェック
    if model.time / 1000 > now:
        raise HTTPException(400, detail="Your watch is too bad lol")

    # セッション情報保存
    token = secrets.token_urlsafe(32)

    while True:
        authCode = randomAuthCode(6)
        if not await DBService.redis.get(f"sonolus:reverseAuth:{authCode}"):
            break

    await DBService.redis.set(
        f"sonolus:user:{token}", model.userProfile.model_dump_json(), 60 * 5
    )
    await DBService.redis.set(f"sonolus:authCode:{token}", authCode, 60 * 5)
    await DBService.redis.set(
        f"sonolus:reverseAuth:{authCode}", model.userProfile.model_dump_json(), 60 * 5
    )

    return ServerAuthenticateResponse(
        session=token, expiration=int((now + 60 * 5) * 1000)
    )
