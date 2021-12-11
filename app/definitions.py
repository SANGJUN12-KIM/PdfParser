from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).absolute().parent.parent
CONVERTED_DIR = Path(__file__).absolute().parent.parent.joinpath('converted')
TEMP_DIR = Path(__file__).absolute().parent.parent.joinpath('tmp')
LIBS_DIR = Path(__file__).absolute().parent.parent.joinpath('libs')

