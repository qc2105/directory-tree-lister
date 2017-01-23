import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(packages=[], excludes=[])

if sys.platform.startswith('win32'):
    base = 'Win32GUI'
    icon = 'resources/icon.ico'
    executable = 'dtlister\\__init__.py'
else:
    base = None
    icon = None
    executable = 'dtlister/__init__.py'

executables = [
    Executable(executable, base=base, icon=icon)
]

setup(
    name='Directory Tree Lister',
    version='0.9',
    author='spottywolf',
    description='Creates a recursive list of a directory and saves it as either a text or excel file.',
    options=dict(build_exe=buildOptions),
    executables=executables
)
