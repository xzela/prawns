from django.db import models

# Create your models here.
VIDEO_STATUS = (
    ('active', 'Active'),
    ('deleted', 'Deleted')
)

CATEGORY_TYPE = (
    ('all', 'All'),
    ('straight', 'Straight'),
    ('gay', 'Gay'),
    ('ts', 'Trans')
)

PHOTO_SIZES = (
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('medium1', 'Medium 1'),
    ('medium2', 'Medium 2'),
    ('big', 'Big')
)


class Videos(models.Model):
    redtube_id = models.IntegerField(max_length=11, unique=True)
    insert_date = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=255)
    status = models.CharField(max_length=11, choices=VIDEO_STATUS)
    title = models.CharField(max_length=255, null=True)
    rating = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    number_of_ratings = models.IntegerField(max_length=11, null=True)
    publish_date = models.DateTimeField()
    duration = models.CharField(max_length=11, null=True)
    number_of_views = models.IntegerField(max_length=11, null=True)
    embed_code = models.TextField(null=True)
    # category = models.TextField(choices=CATEGORIES)

    def thumb_url(self):
        random_image = VideoPhotos.objects.filter(video=self.id).order_by('?')[0].url
        return random_image


class Categories(models.Model):
    insert_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255, choices=CATEGORY_TYPE)

    class Meta:
        unique_together = ('title', 'content_type')


class VideoPhotos(models.Model):
    insert_date = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Videos)
    filename = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    size = models.CharField(max_length=24, choices=PHOTO_SIZES)
    width = models.IntegerField(max_length=11)
    height = models.IntegerField(max_length=11)

    class Meta:
        unique_together = ('video', 'filename')


class Tags(models.Model):
    insert_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, unique=True)
    url_string = models.CharField(max_length=255, unique=True)
    original = models.CharField(max_length=255, unique=True)

    def image_url(self):
        random_video = VideoTags.objects.filter(tag=self.id).order_by('?')[0]
        image_url = VideoPhotos.objects.filter(video=random_video.video_id).order_by('?')[0].url
        return image_url


class VideoTags(models.Model):
    insert_date = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Videos)
    tag = models.ForeignKey(Tags)

    class Meta:
        unique_together = ('video', 'tag')
