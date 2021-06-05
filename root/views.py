from django.shortcuts import render

from root.utils import Firestore
from google.cloud import storage
import os

db = Firestore("file-sorting-root-tracking")

prefixes = ["2460", "2461", "2462", "2463", "2464", "2465"]
delimiter = '/'
storage_client = storage.Client()


def home(request):
    return render(request, 'root/home.html')


def images(request):
    if request.GET.get('exp') is not None:

        exp = request.GET.get('exp')
        qr_num = exp.split('.')[0]
        seed_num = exp.split('.')[1]
        seed_context = None

        doc = db.get('root', qr_num)

        seeds = doc.get('seeds')
        for seed in seeds:
            if seed.get('seed_number') == int(seed_num):
                seed_context = seed

        context = {'exp': doc, 'seed': seed_context}

        return render(request, 'root/image-details.html', context)

    context = {'image_urls': get_image_urls()}

    return render(request, 'root/images.html', context)


def internal(request):
    return render(request, 'root/internal.html')


def blog(request):
    return render(request, 'root/blog.html')


def get_image_urls():
    image_urls = []
    for prefix in prefixes:

        blobs = storage_client.list_blobs('root-tracking-public', prefix=f'showcase/{prefix}/', delimiter=delimiter)

        for blob in blobs:
            # is_public = "READER" in blob.acl.all().get_roles()
            public_url = blob.public_url
            filename, ext = os.path.splitext(public_url)

            if "germination" in filename:
                box_num = os.path.basename(os.path.dirname(filename))
                seed_num = os.path.basename(filename)[-1:]
                image_urls.append({"url": public_url, "box_num": box_num, "seed_num": seed_num})
    return image_urls
