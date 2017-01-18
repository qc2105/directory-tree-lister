import collections
import os
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


def list_directory_tree(directory: str) -> None:
    """
    Writes a recursive list of a directory with files sizes in an xlsx file.

    :param directory: a directory to be recursive listed
    :type directory: str
    """
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('directory-list.xlsx')
    worksheet = workbook.add_worksheet()
    time_created = '{} {}'.format(time.strftime("%d/%m/%Y"), time.strftime('%H:%M:%S'))

    row = 0
    col = 0

    # Write head
    head = (
        'Directory Tree Lister',
        'Version 1.0 - January 2017',
        'Created by spottywolf',
        '(Website)',
        '(Email)',
    )

    for entry in head:
        worksheet.write(row, col, entry)
        row += 1
    row += 1

    # Write header
    header = (
        ['Directory:', directory],
        ['Creation Time:', time_created]
    )

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

    directory_tree = recursive_scandir(directory)

    # Walk the directory tree
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
                line_directory = []
                line_file = []

                for entity in entities:
                    entity_path = os.path.join('{path}/{entity}'.format(path=entry.path, entity=entity))

                    # Entity is a Directory
                    if os.path.isdir(entity_path):
                        line_directory += (('Directory', entity),)
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
                            line_file += (('File', entity, file_size, byte),)

                # Print to document
                line_directory.sort()
                for dr, en in line_directory:
                    worksheet.write(row, col, dr)
                    worksheet.write(row, col + 1, en)
                    row += 1

                line_file.sort()
                for fl, en, size, unit in line_file:
                    worksheet.write(row, col, fl)
                    worksheet.write(row, col + 1, en)
                    worksheet.write(row, col + 2, size)
                    worksheet.write(row, col + 3, unit)
                    row += 1
    workbook.close()


if __name__ == '__main__':
    input_dir = input('Input a directory for scanning: ')
    list_directory_tree(input_dir)
