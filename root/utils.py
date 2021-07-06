"""
    Module consisting of helper classes to support django server logic
"""

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage

import datetime
import dateutil.parser
from urllib import parse

from django.utils import timezone


class Firestore:

    def __init__(self, project_id : str):
        if len(firebase_admin._apps) < 1:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': project_id,
            })

        self.db = firestore.client()

    def put(self, collection, doc, data, merge):
        doc_ref = self.db.collection(collection).document(doc)
        doc_ref.set(data, merge=merge)

    def get(self, collection, doc):
        doc_ref = self.db.collection(collection).document(doc)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print("document not found")
            return None

    def update(self, collection, doc, data):
        doc_ref = self.db.collection(collection).document(doc)
        doc_ref.update(data)

    def query(self, collection, key, value, comparator):
        return self.db.collection(collection).where(key, comparator, value).stream()

class Bucket:

    def __init__(self, bucket_name):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)

    def generate_download_signed_url_v4(self, blob_name, time_valid_min):
        """Generates a v4 signed URL for downloading a blob.

        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.
        """
        # bucket_name = 'your-bucket-name'
        # blob_name = 'your-object-name'

        blob = self.bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=datetime.timedelta(minutes=time_valid_min),
            # Allow GET requests using this URL.
            method="GET",
        )
        return url



class ImageContext:
    """
        Data model to describe an image on the /gallery page
    """

    def __init__(self, url, box_num, seed_num):
        # instance attributes
        self.url = url
        self.box_num = box_num
        self._seed_num = seed_num

    def is_url_expired(self) -> bool:
        expires_seconds = parse.parse_qs(parse.urlparse(self.url).query)['X-Goog-Expires'][0]
        start_date_iso = parse.parse_qs(parse.urlparse(self.url).query)['X-Goog-Date'][0]
        expire_date_iso = dateutil.parser.parse(start_date_iso) + datetime.timedelta(
            seconds=float(expires_seconds))
        return timezone.now() > expire_date_iso

    def get_exp_id(self) -> str:
        return f'{self.box_num}.{self.seed_num}'

    @staticmethod
    def as_exp_id(box_num, seed_num) -> str:
        return f'{box_num}.{seed_num}'

    @classmethod
    def from_exp_id(cls, url, exp_id):
        return cls(url, exp_id.split['.'][0], exp_id.split['.'][1])

    @property
    def seed_num(self):
        return self._seed_num

    @seed_num.setter
    def seed_num(self, value):
        if int(value) > 0 and isinstance(value, str):
            self._seed_num = value
        else:
            raise ValueError('seed_num value must be > 0')

    def to_dict(self) -> dict:
        return {'url': self.url, 'box_num': self.box_num, 'seed_num': self.seed_num}

class Cache:
    """
        A dictionary implementation to cache signed_urls of ImageContext data
    """

    # class attributes
    bucket = Bucket('file-sorting-data')
    bucket_path = 'Anupam/showcase/showcase/{}/hist.png'

    def __init__(self):
        # instance attributes
        self.signed_urls = {}

    def get(self, box_num, seed_num) -> ImageContext:
        return self.signed_urls.get(ImageContext.as_exp_id(box_num, seed_num))

    def contains(self, box_num, seed_num) -> bool:
        return ImageContext.as_exp_id(box_num, seed_num) in self.signed_urls

    def is_expired(self, box_num, seed_num) -> bool:
        return self.get(box_num, seed_num).is_url_expired()

    def update(self, box_num, seed_num) -> ImageContext:
        url = self.bucket.generate_download_signed_url_v4(self.bucket_path.format(box_num), 10)
        context = ImageContext(url, box_num, seed_num)
        self.signed_urls[context.get_exp_id()] = context
        return context
