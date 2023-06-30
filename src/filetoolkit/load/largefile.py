import pathlib
from typing import Union

from tqdm import tqdm
from jafdecs import worm

from ..utilities import chunksize


def read(path: Union[str, pathlib.Path]) -> bytes:
    return LargeFileReader(path=path)


@worm.onproperties
class LargeFileReader:
    def __init__(self, path: Union[pathlib.Path, str]):
        self.path = pathlib.Path(path)
    
    @property
    def progress(self):
        return tqdm(
            total=self.path.stat().st_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=f'Loading {self.path.name}'
        )
    
    @property
    def file(self):
        return self.path.open('rb')
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def read(self, *args, **kwargs) -> bytes:
        if len(args) > 0 or len(kwargs) > 0:
            response = self.file.read(*args, **kwargs)
            self.progress.update(len(response))
        
        else:
            response = b''
            for chunk in chunksize.optimal(self.path):
                self.progress.update(len(chunk))
                response += chunk
        
        return response

    def readline(self, *args, **kwargs) -> bytes:
        response = self.file.readline(*args, **kwargs)
        self.progress.update(len(response))
        return response
