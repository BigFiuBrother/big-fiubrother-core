# big-fiubrother-core-video-storage

Submodule of *big-fiubrother-core* to handle the storage of binary information, more
specifically video chunks. Currently, the video chunks are stored in S3 filesystem,
divided in two buckets:
- *raw-video-chunks*
- *processed-video-chunks*

## Usage

```python
from big_fiubrother_core_video_storage import get_raw_storage, get_processed_storage

# Configuration for S3 storage
configuration = {
    'host': 'localhost',
    'port': 9500,
    'access_key': 'fiubrother',
    'secret_key': '1234'
}

# Fetch file with id from raw video_storage. Store it in filepath
raw_storage = get_raw_storage(configuration)
raw_storage.retrieve_file('id', 'filepath')

# Process video in filepath
# ...

# Store processed file in filepath into the processed video_storage. 
processed_storage = get_processed_storage(configuration)
processed_storage.store_file('id', 'filepath')
```