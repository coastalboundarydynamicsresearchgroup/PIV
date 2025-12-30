import sys
import time
from shutil import make_archive

dataPathRoot = '/piv/data/'
archivePathRoot = '/piv/archive/'


def zipDataset(datasetName):
  global dataPathRoot
  global archivePathRoot

  utcDateTime = time.gmtime()
  archiveFilename = "dataset_{dataset}_{year:04d}-{month:02d}-{day:02d}_{hour:02d}.{minute:02d}.{second:02d}".format(dataset=datasetName, year=utcDateTime.tm_year, month=utcDateTime.tm_mon, day=utcDateTime.tm_mday, hour=utcDateTime.tm_hour, minute=utcDateTime.tm_min, second=utcDateTime.tm_sec)
  make_archive(base_name=archivePathRoot + archiveFilename, format="zip", root_dir=dataPathRoot+datasetName, base_dir='.' )

  return archiveFilename

datasetName = sys.argv[1] if len(sys.argv) > 1 else None

archiveFilename = zipDataset(datasetName)

# Return to caller on stdout
response = '{"filename": "' + archiveFilename +'"}'
print(response)
