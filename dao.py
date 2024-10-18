from typing import Any, TextIO, List, Tuple
from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from hash import calculate_hash, HASH_ALGORITHMS

'''
    功能点说明
    1.可以添加字典
    2.可以查询密文值类型和对应明文
    3.可以查询明文对应密文类型或计算对应密文
'''

engine = create_engine("sqlite:///./hash.db", echo=False)


class Base(DeclarativeBase):
    pass


#建表过程
class Hash(Base):
    __tablename__ = 'hash'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(nullable=True)
    MD5: Mapped[str] = mapped_column(nullable=True)
    SHA1: Mapped[str] = mapped_column(nullable=True)
    SM3: Mapped[str] = mapped_column(nullable=True)
    SHA224: Mapped[str] = mapped_column(nullable=True)
    SHA256: Mapped[str] = mapped_column(nullable=True)
    SHA384: Mapped[str] = mapped_column(nullable=True)
    SHA512: Mapped[str] = mapped_column(nullable=True)
    SHA3_224: Mapped[str] = mapped_column(nullable=True)
    SHA3_256: Mapped[str] = mapped_column(nullable=True)
    SHA3_384: Mapped[str] = mapped_column(nullable=True)
    SHA3_512: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return (f"Hash(id={self.id!r}, \n"
                f"MD5={self.MD5!r},"
                f"SHA1={self.SHA1!r},\n"
                f"SM3={self.SM3!r},\n"
                f"SHA224={self.SHA224!r},\n"
                f"SHA256={self.SHA256!r},\n"
                f"SHA384={self.SHA384!r},\n"
                f"SHA512={self.SHA512!r},\n"
                f"SHA3_224={self.SHA3_224!r},\n"
                f"SHA3_256={self.SHA3_256!r},\n"
                f"SHA3_384={self.SHA3_256!r},\n"
                f"SHA3_512={self.SHA3_512!r})")


# Base.metadata.create_all(engine) #创建表


def read_large_file(file_object):
    """使用生成器读取文件,减少内存消耗"""
    for line in file_object:
        yield line.strip()


def exist(message: str, session) -> bool:
    """判断数据是否存在"""
    result = session.execute(select(Hash.message).filter_by(message=message)).first()
    return result is not None


def process_data(message: str) -> Any:
    """封装数据"""
    hash_data = {alog_name.upper(): calculate_hash(alog_name, message) for alog_name in HASH_ALGORITHMS}
    return Hash(message=message, **hash_data)


def get_data_len(session) -> int:
    """统计数据库中当前的记录条目"""
    return session.query(Hash.id).count()


def insert_bulk(file: TextIO, session: Any, batch_size: int = 1000) -> bool:
    """用于批量保存hash数据"""
    batch_data = []
    initial_count = get_data_len(session)
    for message in read_large_file(file):
        if exist(message, session):
            print(f'{message}已存在')
            continue
        else:
            data = process_data(message)
            batch_data.append(data)
        # 当数据量达到 BATCH_SIZE 时，执行一次批量插入
        if len(batch_data) >= batch_size:
            session.add_all(batch_data)  # 批量插入
            session.commit()
            batch_data = []  # 清空批量数据列表
        # 插入剩余未达到 BATCH_SIZE 的数据
    if batch_data:
        session.add_all(batch_data)
        session.commit()
    final_count = get_data_len(session)
    inserted_count = final_count - initial_count
    if inserted_count:
        print(f'插入完成\n原有{initial_count}条记录\n现有{final_count}\n成功插入 {inserted_count} 条记录。')
        return True
    else:
        print(f'插入失败：插入 {inserted_count} 条记录。')


def insert(filename: str) -> None:
    """插入hash数据"""
    with Session(engine) as session:
        try:
            with open(filename, 'r') as file:
                insert_bulk(file, session)
        except FileNotFoundError:
            print(f'{filename}不存在，或路径有误')
        except Exception as e:
            print(f'发生错误：{e}')  # 捕获其他异常并打印


def display_message(result, fields) -> None:
    """
       将查询结果与字段名进行配对并打印
       :param result: 查询返回的值 (元组)
       :param fields: 字段名称的列表
       """
    for field, value in zip(fields, result):
        print(f'{field}: {value}')


def display_cipher(value, result, fields) -> None:
    message = result[0]
    for hash_value, hash_attr in zip(result[1:], fields):
        if hash_value == value:
            print(f'hash值类型: {hash_attr}')
            print(f'明文: {message}')
            break


def look_message(value: str, fields: List[str]):
    HASH_ATTR = [getattr(Hash, attr.upper()) for attr in fields]
    with Session(engine) as session:
        result = session.execute(select(*HASH_ATTR).filter_by(message=value)).first()
    if result is not None:
        display_message(result, fields)
    else:
        result = (calculate_hash(field, value) for field in fields)
        display_message(result, fields)


def look_cipher(value: str, fields: List[str]) -> None:
    HASH_ATTR = [getattr(Hash, attr.upper()) for attr in fields]
    conditions = [attr == value for attr in HASH_ATTR]

    with Session(engine) as session:
        result = session.execute(select(Hash.message, *HASH_ATTR).filter(or_(*conditions))).first()

    if result is not None:
        display_cipher(value, result, fields)
    else:
        print(f'库中没有 {value} 的 hash 数据记录')


def look(value: str, fields: List[str] = HASH_ALGORITHMS, is_msg=False):
    if is_msg:
        print(f'查询明文值：{value}')
        look_message(value, fields)
    else:
        print(f'查询密文值：{value}')
        look_cipher(value, fields)
