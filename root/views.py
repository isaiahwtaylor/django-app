from django.shortcuts import render, redirect
from django.http import JsonResponse

from root.utils import Firestore, Bucket, Cache
import os
import json

db = Firestore("file-sorting-root-tracking")
b = Bucket('file-sorting-data')

prefixes = ["2460", "2461", "2462", "2463", "2464", "2465"]
delimiter = '/'

cache = Cache()
processed_video_cache = Cache(bucket_name='processed-image-files', bucket_path='videos/{}.mp4')
archive_cache = Cache(bucket_name='root-images-archive', bucket_path='finished_exp/{}.zip')


def about(request):
    return render(request, 'root/about.html')


def home(request):
    return render(request, 'root/home.html')


def gallery(request):
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
            # FIXME remove
            get_processed_video_urls()
        context = {'image_urls': image_urls}
        return render(request, 'root/images.html', context)

    context = {'image_urls': get_image_urls()}

    return render(request, 'root/images.html', context)


def internal(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        box_num = data.get('box_num')
        seed_num = data.get('seed_num')
        if data.get('type') == 'zip':
            # return signed url to download archive
            if archive_cache.contains(box_num, seed_num) and not archive_cache.is_expired(box_num, seed_num):
                image_context = archive_cache.get(box_num, seed_num)
            else:
                image_context = archive_cache.update(box_num, seed_num)
            return JsonResponse({'url': image_context.url})

        doc = db.get('root', box_num)
        seeds = doc.get('seeds')
        for seed in seeds:
            if seed.get('seed_number') == int(seed_num):
                return JsonResponse({'tip_coords': seed.get('tip_coords')})

        return JsonResponse({'tip_coords': None})
    if request.user.is_superuser or is_guest_group(request.user):
        unsorted, length = get_unsorted_experiments()
        # image_urls = get_union(get_processed_video_urls(), get_archive_video_frames())

        context = {'image_urls': get_processed_video_urls(), 'unsorted': unsorted, 'unsorted_length': length}
        return render(request, 'root/internal.html', context)
    else:
        return redirect('/login')


def blog(request):
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
                if (box_num != '2463' or seed_num != '1') and (box_num != '2465' or seed_num != '3'):
                    image_urls.append({"url": public_url, "box_num": box_num, "seed_num": seed_num})
    return image_urls


def get_processed_video_urls():
    blobs = b.storage_client.list_blobs('processed-image-files', prefix='videos/', delimiter=delimiter)
    image_urls = []
    for blob in blobs:
        box_num = os.path.splitext(os.path.basename(blob.name))[0]
        # FIXME unused seed_num
        seed_num = 0

        if processed_video_cache.contains(box_num, seed_num) and not processed_video_cache.is_expired(box_num,
                                                                                                      seed_num):
            image_context = processed_video_cache.get(box_num, seed_num)
        else:
            image_context = processed_video_cache.update(box_num, seed_num)
        image_urls.append(image_context.to_dict())
        print(processed_video_cache.get(box_num, seed_num).to_dict())
    return image_urls


def get_archive_video_frames():
    blobs = b.storage_client.list_blobs('root-images-archive', prefix='finished_exp/', delimiter=delimiter)
    zip_urls = []
    for blob in blobs:
        box_num = os.path.splitext(os.path.basename(blob.name))[0]
        # FIXME unused seed_num
        seed_num = 0

        if archive_cache.contains(box_num, seed_num) and not archive_cache.is_expired(box_num, seed_num):
            image_context = archive_cache.get(box_num, seed_num)
        else:
            image_context = archive_cache.update(box_num, seed_num)
        zip_urls.append(image_context.to_dict())
        print(archive_cache.get(box_num, seed_num).to_dict())
    return zip_urls


def get_union(image_urls, archive_urls):
    result = []
    for x in image_urls:
        num = x.get('box_num')
        for y in archive_urls:
            if y.get('box_num') == num:
                x['url_zip'] = y.get('url')
        result.append(x)
    return result


def get_unsorted_experiments():
    unsorted = []
    length = 0
    robots = ['robot1', 'robot2', 'robot3', 'robot4']
    for prefix in robots:

        blobs = b.storage_client.list_blobs('file-sorting-data', prefix=f'unsorted_unlabeled/{prefix}/',
                                            delimiter=delimiter)

        for blob in blobs:
            filename, ext = os.path.split(blob.name)
            robot = os.path.split(filename)[1]
            if ext is not '':
                length += 1
                x = Unsorted.search(unsorted, robot)
                if x is not None:
                    x.data.append(ext)
                else:
                    u = Unsorted(robot)
                    u.data.append(ext)
                    unsorted.append(u)
    return unsorted, length


class Unsorted:
    def __init__(self, name):
        self.name = name
        self.data = []

    def contains(self, value) -> bool:
        if value in self.data:
            return True
        else:
            return False

    @staticmethod
    def search(arr: list, obj) -> 'Unsorted':
        for i in arr:
            if obj == i.name:
                return i


def is_guest_group(user):
    return user.groups.filter(name='guest').exists()
