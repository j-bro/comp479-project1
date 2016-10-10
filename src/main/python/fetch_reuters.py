import wget
import tarfile

url = 'http://www.daviddlewis.com/resources/testcollections/reuters21578/reuters21578.tar.gz'
filename = wget.download(url)

untar_dir = 'reuters21578'
tar = tarfile.open(filename)
tar.extractall(path=untar_dir)
tar.close()
