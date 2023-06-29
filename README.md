# FileToolkit

This repository contains a Python 3 package offering some file tools that I have found useful in the past:

* Progress bar showing progress of reading a file into memory
* Loading a collection of files onto a RAM disk for faster processing


## Installation

To install the entire toolkit:

```
pip install filetoolkit
```

For only individual tools:

```
pip install filetoolkit[ramdisk]
pip install filetoolkit[bigfileload]
```


## Usage

```
import filetoolkit
```

### RAM disk

Example:

```
from filetoolkit import ramdisk
# TBD.
```

Result:

```
TBD.
```


### Progress Bar for Reading Big Files

Example:

```
import json
from filetoolkit import load
with load.readlargefile('2GB.json') as file:
    v = json.load(file)
    # ...
```

Result:

```
TBD.
```
