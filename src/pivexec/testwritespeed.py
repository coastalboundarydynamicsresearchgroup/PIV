import time
import os

def writeFile(filename, sizeInMB):
    """Writes a file of specified size in MB to test write speed."""
    chunkSize = 1024 * 1024  # 1 MB
    totalChunks = sizeInMB

    with open(filename, 'wb') as f:
        for _ in range(totalChunks):
            f.write(b'\0' * chunkSize)


def testWriteSpeed(directory, filecount, fileSizeMB):
    """Tests write speed by writing multiple files of specified size."""

    if not os.path.exists(directory):
        os.makedirs(directory)

    startTime = time.time()

    for i in range(filecount):
        filename = os.path.join(directory, f'testfile_{i}.dat')
        writeFile(filename, fileSizeMB)

    endTime = time.time()
    totalTime = endTime - startTime
    totalData = filecount * fileSizeMB  # in MB
    speed = totalData / totalTime  # in MB/s

    print(f"Total data written: {totalData} MB")
    print(f"Total time taken: {totalTime:.2f} seconds")
    print(f"Write speed: {speed:.2f} MB/s")
