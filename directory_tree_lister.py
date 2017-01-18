import collections
import os
import textwrap
import time

import xlsxwriter


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


def format_file_size(file_size: float) -> tuple:
    """
    Format file size for readability.

    :param file_size: size of file
    :type file_size: float
    :return: file size formatted to 2 decimals and the corresponding data unit
    :rtype: tuple(float, str)
    """
    Bytes = collections.namedtuple('Bytes', ['kilobyte', 'megabyte', 'gigabyte', 'terabyte'])
    b = Bytes(kilobyte=1000, megabyte=1000000, gigabyte=1000000000, terabyte=1000000000000000)

    if file_size < b.kilobyte:
        file_size = round(file_size, 2)
        unit = 'B'
    elif b.kilobyte <= file_size < b.megabyte:
        file_size = round(file_size / b.kilobyte, 2)
        unit = 'KB'
    elif b.megabyte <= file_size < b.gigabyte:
        file_size = round(file_size / b.megabyte, 2)
        unit = 'MB'
    elif b.gigabyte <= file_size < b.terabyte:
        file_size = round(file_size / b.gigabyte, 2)
        unit = 'GB'
    else:
        file_size = round(file_size / b.terabyte, 2)
        unit = 'TB'
    return file_size, unit


def list_directory_tree_text(directory: str) -> None:
    """
    Writes a recursive list of a directory with files sizes in a text file.

    :param directory: a directory to be recursive listed
    :type directory: str
    """
    file_name = directory.split('/')[-1]
    output_file = '{path}/{file}'.format(path=os.path.dirname(os.path.abspath(__file__)),
                                         file='directory-tree-{}.txt'.format(file_name))
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

    # Walk the directory tree
    directory_tree = recursive_scandir(directory)

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
                directories = []
                files = []

                for entity in entities:
                    entity_path = os.path.join('{path}/{entity}'.format(path=entry.path, entity=entity))

                    # Entity is a Directory
                    if os.path.isdir(entity_path):
                        directories += ['{type:<15}{title:<120}'.format(type='Directory', title=entity)]
                    # Entity is a File
                    else:
                        if entity[0] != '.':
                            file_size = os.stat(entity_path).st_size

                            file_size, unit = format_file_size(file_size)
                            files += ['{type:<15}{title:<120}{size:8.2f}{byte:>3}'.format(
                                type='File', title=entity, size=file_size, byte=unit)]

                # Print to document
                directories.sort()
                for directory in directories:
                    print(directory, file=f)

                files.sort()
                for file in files:
                    print(file, file=f)
        # Add new line at the end of entry
        print('', file=f)


def list_directory_tree_excel(directory: str) -> None:
    """
    Writes a recursive list of a directory with files sizes in an xlsx file.

    :param directory: a directory to be recursive listed
    :type directory: str
    """
    # Create a workbook and add a worksheet.
    file_name = directory.split('/')[-1]
    workbook = xlsxwriter.Workbook('directory-tree-{}.xlsx'.format(file_name))
    worksheet = workbook.add_worksheet()
    time_created = '{} {}'.format(time.strftime("%d/%m/%Y"), time.strftime('%H:%M:%S'))

    row = 0
    col = 0

    # Head and Header
    head = (
        'Directory Tree Lister',
        'Version 1.0 - January 2017',
        'Created by spottywolf',
        '(Website)',
        '(Email)',
    )

    header = (
        ('Directory:', directory),
        ('Creation Time:', time_created),
    )

    for entry in head:
        worksheet.write(row, col, entry)
        row += 1
    row += 1

    for entry, entry_value in header:
        worksheet.write(row, col, entry)
        worksheet.write(row, col + 1, entry_value)
        row += 1
    row += 1

    # Write entry types
    worksheet.write(row, col, 'Type')
    worksheet.write(row, col + 1, 'Title')
    worksheet.write(row, col + 2, 'File Size')
    worksheet.write(row, col + 3, 'Size Unit')
    row += 1

    # Walk the directory tree
    directory_tree = recursive_scandir(directory)

    for entry in directory_tree:
        if entry.is_dir(follow_symlinks=False):
            row += 1
            worksheet.write(row, col, entry.path)
            row += 1

            # Entities within Directory
            entities = os.listdir(entry.path)

            # Directory is empty, excludes .ds_store file
            if len(entities) == 1 and entities[0][0] == '.':
                worksheet.write(row, col, '-- Empty Directory --')
                row += 1
            # Directory is not empty
            else:
                directories = []
                files = []

                for entity in entities:
                    entity_path = os.path.join('{path}/{entity}'.format(path=entry.path, entity=entity))

                    # Entity is a Directory
                    if os.path.isdir(entity_path):
                        directories += (entity,)
                    # Entity is a File
                    else:
                        if entity[0] != '.':
                            file_size = os.stat(entity_path).st_size
                            file_size, unit = format_file_size(file_size)

                            files += ((entity, file_size, unit),)

                # Print to document
                directories.sort()
                for directory in directories:
                    worksheet.write(row, col, 'Directory')
                    worksheet.write(row, col + 1, directory)
                    row += 1

                files.sort()
                for name, file_size, unit in files:
                    worksheet.write(row, col, 'File')
                    worksheet.write(row, col + 1, name)
                    worksheet.write(row, col + 2, file_size)
                    worksheet.write(row, col + 3, unit)
                    row += 1
    workbook.close()


if __name__ == '__main__':
    input_directory = input('Input a directory for scanning: ')

    while True:
        output_type = input(textwrap.dedent('''
        Select out type:
        1) Text - .txt
        2) Excel - xlsx
        '''))

        if output_type == '1':
            list_directory_tree_text(input_directory)
            print('')
            break
        elif output_type == '2':
            list_directory_tree_excel(input_directory)
            break
