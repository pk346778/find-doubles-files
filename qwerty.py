import os
import pprint


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
    pprint.pprint(walk('/home/qiwi/'))

if __name__ == '__main__':
    main()
