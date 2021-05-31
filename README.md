# django-app

[![codecov](https://codecov.io/gh/aaronBioBot/django-app/branch/main/graph/badge.svg?token=NFMKNPAS0N)](https://codecov.io/gh/aaronBioBot/django-app)

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

### Testing

```$ python manage.py runserver```

```localhost:8000```

