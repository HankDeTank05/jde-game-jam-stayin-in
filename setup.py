from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ['arcade'], excludes = [], include_files = ['sprites/log'])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, targetName = 'lumberjack_partners')
]

setup(name='lumberjack partners',
      version = '1.0',
      description = "a game by Henry Holman for the Stayin' In JDE Game Jam",
      options = dict(build_exe = buildOptions),
      executables = executables)
