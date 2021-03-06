# django-app

[![codecov](https://codecov.io/gh/aaronBioBot/django-app/branch/main/graph/badge.svg?token=NFMKNPAS0N)](https://codecov.io/gh/aaronBioBot/django-app)
[![django-test workflow](https://github.com/aaronBioBot/django-app/actions/workflows/django-test.yml/badge.svg)](https://github.com/aaronBioBot/django-app/actions/workflows/django-test.yml)
[![django-deploy workflow](https://github.com/aaronBioBot/django-app/actions/workflows/django-deploy.yml/badge.svg)](https://github.com/aaronBioBot/django-app/actions/workflows/django-deploy.yml)
![django-v3.2](https://img.shields.io/static/v1?label=&message=3.2&color=214a35&logo=django)

###  https://file-sorting-root-tracking.uc.r.appspot.com/

Website to view root image analysis, powered by django.

### Services

* Hosting 
    * GCP App Engine Standard
* Storage 
    * Cloud Storage Buckets
    * Firestore
    * Cloud SQL

### Deployment

```$ python manage.py collectstatic```

```$ gcloud app deploy```

### Run Locally

```$ python manage.py runserver```

Go to ```localhost:8000```

### Unit Testing

```$ python manage.py test```

### Content

* Blog
  * Edit Pages in Markdown and upload to ```/templates/root/blogs/md```
  * Run node script ```$ node app.js``` to convert markdown to html