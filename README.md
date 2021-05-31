# django-app

[![codecov](https://codecov.io/gh/aaronBioBot/django-app/branch/main/graph/badge.svg?token=NFMKNPAS0N)](https://codecov.io/gh/aaronBioBot/django-app)
![django-test workflow](https://github.com/aaronBioBot/django-app/actions/workflows/django-test.yml/badge.svg)
![django-deploy workflow](https://github.com/aaronBioBot/django-app/actions/workflows/django-deploy.yml/badge.svg)
![django-v3.2](https://img.shields.io/static/v1?label=&message=3.2&color=214a35&logo=django)

###  https://file-sorting-root-tracking.uc.r.appspot.com/

Website to view root image analysis, powered by django.

### Services

* Hosting 
    * GCP App Engine Standard
* Storage 
    * Cloud Storage Buckets
    * Firestore

### Deployment

```$ python manage.py collectstatic```

```$ gcloud app deploy```

### Run Locally

```$ python manage.py runserver```

```localhost:8000```

### Unit Testing

```$ python manage.py test```
