from django.shortcuts import render, redirect
from django.http import JsonResponse

from root.utils import Firestore, Bucket, ImageContext, Cache
import os
import json

from urllib import parse
import dateutil.parser
import datetime
from django.utils import timezone

db = Firestore("file-sorting-root-tracking")
b = Bucket('file-sorting-data')


prefixes = ["2460", "2461", "2462", "2463", "2464", "2465"]
delimiter = '/'

# find element in unordered list O(n), find element in set is O(1)
# set does not have key:value pairs
# no literals for set, {} reserved for dict
# signed_urls = {}
cache = Cache()



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
    elif request.GET.get('date') is not None and request.GET.get('date') is not "":
        docs = db.query('root', 'date_planted', request.GET.get('date').replace('-', '/'), '>=')
        image_urls = []
        for doc in docs:
            seed_count = len(doc.to_dict().get('seeds'))
            for x in range(seed_count):
                image_urls.append({"url":
                                       f"https://storage.googleapis.com/root-tracking-public/showcase/{doc.id}/"
                                       f"germination_seed{str(x + 1)}.png",
                                   "box_num": doc.id, "seed_num": str(x + 1)})

        if request.user.is_superuser:
            # TODO loop through experiments in private bucket
            boxes = [{'box_num': '2460', 'seed_num': '1'}, {'box_num': '2461', 'seed_num': '1'}]
            for box in boxes:
                box_num = box.get('box_num')
                seed_num = box.get('seed_num')

                if cache.contains(box_num, seed_num) and not cache.is_expired(box_num, seed_num):
                    image_context = cache.get(box_num, seed_num)
                else:
                    image_context = cache.update(box_num, seed_num)
                image_urls.append(image_context.to_dict())
                print(cache.get(box_num, seed_num).to_dict())

        context = {'image_urls': image_urls}
        return render(request, 'root/images.html', context)

    context = {'image_urls': get_image_urls()}

    return render(request, 'root/images.html', context)


def internal(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            doc = db.get('root', data.get('box_num'))
            seeds = doc.get('seeds')
            for seed in seeds:
                if seed.get('seed_number') == int(data.get('seed_num')):
                    return JsonResponse({'tip_coords': seed.get('tip_coords')})

            return JsonResponse({'tip_coords': None})

        context = {'image_urls': get_image_urls()}
        return render(request, 'root/internal.html', context)
    else:
        return redirect('/login')


def blog(request):
    # Open a file: file
    # file = open('/root/templates/root/blogs/in.md', mode='r')
    #
    # # read all lines at once
    # all_of_it = file.read()
    # print(all_of_it)

    # with open('/root/templates/root/blog.html') as f:
    #     result = f.read()
    #     print(result)
    # close the file
    # file.close()
    if request.GET.get('name') is not None:
        name = request.GET.get('name')
        return render(request, f'root/blogs/html-gen/{name}.html')
    blog_names = []

    print(os.listdir('root/templates/root/blogs'))
    for f in os.listdir('root/templates/root/blogs/html-gen'):
        if f.endswith('.html'):
            print(os.path.splitext(f)[0])
            blog_names.append(os.path.splitext(f)[0])
    context = {'blog_names': blog_names}
    return render(request, 'root/blog.html', context)


def get_image_urls():
    image_urls = []
    for prefix in prefixes:

        blobs = b.storage_client.list_blobs('root-tracking-public', prefix=f'showcase/{prefix}/', delimiter=delimiter)

        for blob in blobs:
            # is_public = "READER" in blob.acl.all().get_roles()
            public_url = blob.public_url
            filename, ext = os.path.splitext(public_url)

            if "germination" in filename:
                box_num = os.path.basename(os.path.dirname(filename))
                seed_num = os.path.basename(filename)[-1:]
                image_urls.append({"url": public_url, "box_num": box_num, "seed_num": seed_num})
    return image_urls
