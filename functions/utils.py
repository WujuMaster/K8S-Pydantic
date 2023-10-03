import base64


def encode_base64(input: str):
    return base64.b64encode(input.encode("ascii")).decode("ascii")
