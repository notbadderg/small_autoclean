import os
from dotenv import find_dotenv, load_dotenv

from utils import CustomException, logger


def get_config() -> dict:
    load_dotenv(find_dotenv())

    params_ = [
        'DST_PATH',
        'MAX_FILES_IN_FOLDER',
        'LOOKING_EXTENSION',
    ]

    cfg_ = {}
    for param in params_:
        value = os.getenv(param)
        if not value:
            raise CustomException(f'Missed {value}')
        cfg_[param] = value

    return cfg_


@logger()
def logger_end():
    return '=' * 20


@logger()
def autoclean(considered_path: str, ext: str, threshold: int) -> dict:
    res = []
    for path, folder, files in os.walk(considered_path):
        [files.remove(k) for k in files if ext != k.split('.')[-1]]
        if len(files) > threshold:
            temp_files = []
            for file in files:
                file_path = os.path.join(path, file)
                e = (file_path, os.path.getmtime(file_path))
                temp_files.append(e)
            temp_files = sorted(temp_files, key=lambda x: x[1], reverse=True)[:len(temp_files) - threshold]
            for removing_file in temp_files:
                os.remove(removing_file[0])
                res.append(removing_file[0])

    return {f'Deleted in {considered_path}: {len(res)}': res}


def main():
    cfg = get_config()
    autoclean(cfg['DST_PATH'], cfg['LOOKING_EXTENSION'], int(cfg['MAX_FILES_IN_FOLDER']))
    logger_end()


if __name__ == '__main__':
    main()
