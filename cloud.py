try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    
from gcloud import storage

client = storage.Client()

filedata = urllib2.urlopen('http://example.com/myfile.txt')
datatoupload = filedata.read()

bucket = client.get_bucket('bucket-id-here')
blob = Blob("myfile.txt", bucket)
blob.upload_from_string(datatoupload)
