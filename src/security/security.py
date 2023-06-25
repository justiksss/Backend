from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

import config


def create_access_token(data: dict , expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITM)

    return encode_jwt