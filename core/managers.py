import os
from django.dispatch import receiver
from django.db import models

def create_filename(instance, filename):
    extension = "." + filename.split(".")[-1] if "." in filename else ""
    try:
        name = instance.name
    except:
        name = instance.id
    kind = instance._meta.model.__name__.lower()
    return f"{kind}-{name.lower()}{extension}".replace(" ", "_")

    
def manage(Model, name, files):
    @receiver(models.signals.post_delete, sender=Model)
    def delete(sender, instance, **kwargs):
        for attr in files:
            try:
                if getattr(instance, attr):
                    if os.path.isfile(getattr(instance, attr).path):
                        os.remove(getattr(instance, attr).path)
            except: pass
    
    @receiver(models.signals.pre_save, sender=Model)
    def save(sender, instance, **kwargs):
        # Get saved version
        if not instance.pk: return False
        try:
            db_obj = sender.objects.get(pk=instance.pk)
        except: return False

        # Should the name be changed?
        if getattr(db_obj, name) != getattr(instance, name):
            for attr in files:
                try:
                    old_path = getattr(instance, attr).path
                    new_name = create_filename(instance, getattr(instance, attr).path)
                    new_path = "/".join(
                    getattr(instance, attr).path.split("/")[:-1]
                    ) + "/" + new_name
                    os.rename(old_path, new_path)
                    setattr(instance, attr, new_name)
                except: pass
        
        # Should the file be deleted
        for attr in files: 
            try:
                new_file = getattr(instance, attr)
                if not getattr(db_obj, attr) == new_file:
                    if os.path.isfile(getattr(db_obj, attr).path):
                        os.remove(getattr(db_obj, attr).path)
            except: pass

    return delete, save