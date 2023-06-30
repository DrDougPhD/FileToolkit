import collections
import pathlib
import time

from . import statistics


def optimal(path: pathlib.Path) -> bytes:
    file_stats = path.stat()
    chunksize = file_stats.st_blksize
    file_size = file_stats.st_size
    size_read = 0
    chunks_read = 0
    m_avg = 0
    growth_factor = 2
    average_bitrate_tracker = collections.deque([float('inf'), float('inf')], maxlen=2)
    optimal_chunksize_found = False

    with path.open('rb') as file:
        while size_read < file_size:
            start = time.time()
            chunk = file.read(chunksize)
            if len(chunk) == 0:
                break

            duration = time.time() - start
            yield chunk

            actual_chunk_size = len(chunk)
            size_read += actual_chunk_size

            # if optimal_chunksize_found:
            #     continue

            # Still searching for optimal chunk size
            byterate = actual_chunk_size / duration
            m_avg = statistics.moving_average(avg=m_avg, n=chunks_read, value=byterate)
            chunks_read += 1

            # import humanfriendly
            # print(f'{chunksize=}: {humanfriendly.format_size(byterate, binary=True)}/sec')
            
            previous_moving_avg = average_bitrate_tracker[-1]
            # print(average_bitrate_tracker)
            if (previous_moving_avg - average_bitrate_tracker[0]) > (m_avg - previous_moving_avg):
                # Rate of growth is decreasing.
                # Optimal chunk size has been found.
                optimal_chunksize_found = True
                # print(f'Optimal {chunksize=}: {humanfriendly.format_size(byterate, binary=True)}/sec')
                continue
            
            average_bitrate_tracker.append(m_avg)
            chunksize *= growth_factor
            growth_factor += 1
