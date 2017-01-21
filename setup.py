import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(
    packages=[],
    excludes=[]
)

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('directory_tree_lister/__init__.py', base=base, targetName='Directory Tree Lister')
]

setup(
    name='Directory Tree Lister',
    version='0.9',
    description='Creates a recursive list of a directory and saves it as either a text or excel file.',
    options=dict(build_exe=buildOptions),
    executables=executables
)
