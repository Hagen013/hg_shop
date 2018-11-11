from core.models import ProductPhoto, ProductPage

def update_thumbnails():
    for instance in ProductPage.objects.all():
        instance.save()
        instance.image.close()
        instance.thumbnail.close()
    
    for instance in ProductPhoto.objects.all():
        instance.save()
        instance.image.close()
        instance.thumbnail.close()
