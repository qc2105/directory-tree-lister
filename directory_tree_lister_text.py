import collections
import os
import textwrap
import time


def recursive_scandir(path: str):
    """
    Generator for recursive os.scandir.

    :param path: path a recursively scan
    :type path: str
    """
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield entry
            yield from recursive_scandir(entry.path)


def list_directory_tree(directory: str) -> None:
    """
    Writes a recursive list of a directory with files sizes in a text file.

    :param directory: a directory to be recursive listed
    :type directory: str
    """
    output_file = '{path}/{file}'.format(path=os.path.dirname(os.path.abspath(__file__)), file='output.txt')
    f = open(output_file, 'w', encoding='utf-8')

    # Header
    print(textwrap.dedent('''
    {style}
    Directory: {directory}
    Creation Time: {time}
    {style}
    Directory Tree Lister
    Version 1.0 - January 2017
    Created by spottywolf
    (Website)
    (Email)
    {style}
    {type:<15}{title:<120}{size:>11}
    ''').format(style='=' * (len(directory) + 11), directory=directory, time='{} {}'.format(
        time.strftime("%d/%m/%Y"), time.strftime('%H:%M:%S')), type='Type', title='Title',
               size='File Size'), file=f)

    directory_tree = recursive_scandir(directory)

    # Walk the directory tree
    for entry in directory_tree:
        if entry.is_dir(follow_symlinks=False):
            print('{styling}\n{current_dir}\n{styling}'.format(styling='=' * len(entry.path), current_dir=entry.path),
                  file=f)

            # Entities within Directory
            entities = os.listdir(entry.path)

            # Directory is empty, excludes .ds_store file
            if len(entities) == 1 and entities[0][0] == '.':
                print('-- Empty Directory --', file=f)
            # Directory is not empty
            else:
                line_directory = []
                line_file = []

                for entity in entities:
                    entity_path = os.path.join('{path}/{entity}'.format(path=entry.path, entity=entity))

                    # Entity is a Directory
                    if os.path.isdir(entity_path):
                        line_directory += ['{type:<15}{title:<120}'.format(type='Directory', title=entity)]
                    # Entity is a File
                    else:
                        if entity[0] != '.':
                            file_size = os.stat(entity_path).st_size

                            Bytes = collections.namedtuple('Bytes', ['kilobyte', 'megabyte', 'gigabyte', 'terabyte'])
                            b = Bytes(kilobyte=1000, megabyte=1000000, gigabyte=1000000000, terabyte=1000000000000000)

                            # format file size for readability
                            if file_size < b.kilobyte:
                                file_size = round(file_size, 2)
                                byte = 'B'
                            elif b.kilobyte <= file_size < b.megabyte:
                                file_size = round(file_size / b.kilobyte, 2)
                                byte = 'KB'
                            elif b.megabyte <= file_size < b.gigabyte:
                                file_size = round(file_size / b.megabyte, 2)
                                byte = 'MB'
                            elif b.gigabyte <= file_size < b.terabyte:
                                file_size = round(file_size / b.gigabyte, 2)
                                byte = 'GB'
                            else:
                                file_size = round(file_size / b.terabyte, 2)
                                byte = 'TB'
                            line_file += ['{type:<15}{title:<120}{size:8.2f}{byte:>3}'.format(
                                type='File', title=entity, size=file_size, byte=byte)]

                # Print to document
                line_directory.sort()
                for dr in line_directory:
                    print(dr, file=f)

                line_file.sort()
                for fl in line_file:
                    print(fl, file=f)

        # Add new line at the end of entry
        print('', file=f)

if __name__ == '__main__':
    input_dir = input('Input a directory for scanning: ')
    list_directory_tree(input_dir)
