import hashlib
import sys
from typing import List

# 定义支持的哈希算法字典

HASH_ALGORITHMS: List[str] = [
    'md5',
    'sha1',
    'sm3',
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512']


def hash_string(alog_name: str, input_data: str) -> str:
    message = input_data.strip().encode('utf-8')
    hash_obj = hashlib.new(alog_name)
    hash_obj.update(message)

    return hash_obj.hexdigest()


def calculate_hash(algo_name: str, input_data: str) -> str:

    if algo_name not in HASH_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algo_name}")
        # 文本处理，将字符串转为字节并更新哈希
    result = hash_string(algo_name, input_data)

    return result


# print(calculate_hash('sm3', '1233'))
