import pathlib
from typing import Union

from tqdm import tqdm


def read(path: Union[str, pathlib.Path]) -> bytes:
    return LargeFileReader(path=path)


class LargeFileReader:
    def __init__(self, path: Union[pathlib.Path, str]):
        self.path = pathlib.Path(path)
        self._progress = None
        self._file = None
    
    @property
    def progress(self):
        if self._progress is None:
            self._progress = tqdm(
                total=self.path.stat().st_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=f'Loading {self.path.name}'
            )
        return self._progress
    
    @property
    def file(self):
        if self._file is None:
            self._file = self.path.open('rb')
        
        return self._file
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def read(self, *args, **kwargs) -> bytes:
        response = self.file.read(*args, **kwargs)
        self.progress.update(len(response))
        return response

    def readline(self, *args, **kwargs) -> bytes:
        response = self.file.readline(*args, **kwargs)
        self.progress.update(len(response))
        return response
