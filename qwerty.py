import os
#import pprint
#import loggin

TARGET_DIR = '/home/qiwi/shared_vb/'
SOURCE_DIR = '/home/qiwi/'


def list_dir(root_dir):
    result = []

    for item in os.listdir(root_dir):
        path = os.path.join(root_dir, item)
        if os.path.isfile(path):
            result.append(path)

    return result


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

    print('start processing...')
    target_files = walk(TARGET_DIR)
    source_files = walk(SOURCE_DIR)

    [print(item) for item in source_files if item not in target_files]

    # pprint.pprint()
    print('end processing...')

if __name__ == '__main__':
    main()
