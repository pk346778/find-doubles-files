import os
import logging
# import pprint

TARGET_DIR = '/home/gunj/Documents/'
SOURCE_DIR = '/home/gunj/Downloads/g-disk'


def walk(root_dir):
    result = []
    for root, dirs, files in os.walk(root_dir):
        if len(files) > 0:
            for file_ in files:
                path = os.path.join(root, file_)
                if os.path.isfile(path):
                    result.append(path)
    return result


def main():

    logging.basicConfig(
        filename='find-missing-files.log',
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
        )

    logging.info('start')
    print('start processing...')
    target_files = walk(TARGET_DIR)
    source_files = walk(SOURCE_DIR)

    list_files = [item for item in source_files if item not in target_files]
    [logging.warn(item) for item in list_files]

    # pprint.pprint(list_files)

    print('end processing...')
    logging.info('end')


if __name__ == '__main__':
    main()
