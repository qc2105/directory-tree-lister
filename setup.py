import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(packages=[], excludes=[])

if sys.platform == 'win32':
    base = 'Win32GUI'
    icon = 'resources/icon.ico'
else:
    base = None
    icon = None

executables = [
    Executable('dtlister/__init__.py', base=base, icon=icon, targetName='Directory Tree Lister')
]

setup(
    name='Directory Tree Lister',
    version='0.9',
    author='spottywolf',
    description='Creates a recursive list of a directory and saves it as either a text or excel file.',
    options=dict(build_exe=buildOptions),
    executables=executables
)
