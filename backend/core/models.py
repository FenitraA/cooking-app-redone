import uuid

from django.db import models


class TimestampedAndStated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=1)

    class Meta:
        abstract = True


class ImageCloudStorage():
    # CDN URL your frontend uses
    image_url = models.CharField(max_length=2048, null=True)
    # Cloudinary public_id OR S3/R2 object_key (super useful for deletes)
    storage_key = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True


class BaseModel(TimestampedAndStated):
    id_prefix = None

    id = models.CharField(
        max_length=128,
        primary_key=True,
        editable=False,
    )

    class Meta:
        abstract = True

    @classmethod
    def generate_id(cls):
        if cls.id_prefix is None:
            raise NotImplementedError(f"{cls.__name__} must define id_prefix")

        return f"{cls.id_prefix}_{uuid.uuid4()}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.__class__.generate_id()

        super().save(*args, **kwargs)


class Counter(BaseModel):
    id_prefix = "counter"

    name = models.CharField(
        max_length=128,
        unique=True,
    )
    current_value = models.IntegerField(default=0)
