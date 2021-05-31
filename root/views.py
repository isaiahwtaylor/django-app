from django.shortcuts import render
from django.http import HttpResponse

from root.utils import Firestore
from google.cloud import storage
import os


db = Firestore("file-sorting-root-tracking")

posts = [
    {
        'author': 'robotmessenger810',
        'temp': 70.0,
        'box_num': 2431,
    },
    {
        'author': 'robotmessenger810',
        'temp': 75.0,
        'box_num': 2432,
    }
]

docs = db.query("root", "date_planted", "01/11/2021")
docs = [doc.to_dict() for doc in docs]

prefixes = ["2460", "2461", "2462", "2463", "2464", "2465"]
delimiter = '/'
storage_client = storage.Client()



image_urls = []

for prefix in prefixes:

    blobs = storage_client.list_blobs('root-tracking-public', prefix=f'showcase/{prefix}/', delimiter=delimiter)

    print("Blobs:")
    for blob in blobs:
        print(blob.name, blob.public_url)
        # is_public = "READER" in blob.acl.all().get_roles()
        if True:
            public_url = blob.public_url
            filename, ext = os.path.splitext(public_url)
            print(filename)
            if "germination" in filename:

                box_num = os.path.basename(os.path.dirname(filename))
                seed_num = os.path.basename(filename)[-1:]

                print(blob.name, public_url)
                image_urls.append({"url": public_url, "box_num": box_num, "seed_num": seed_num})


        if delimiter:
            print("Prefixes:")
            for prefix in blobs.prefixes:
                print(prefix)





def home(request):
    return render(request, 'root/home.html')

def images(request):

    if request.GET.get('exp') is not None:
        print(request.GET.get('exp'))
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

    context = {'posts': docs, 'image_urls': image_urls}

    return render(request, 'root/images.html', context)

# def dashboard(request):
#     return HttpResponse('<h1>Dashboard Page</h1>')

def internal(request):
    return render(request, 'root/internal.html')

def blog(request):
    return render(request, 'root/blog.html')

