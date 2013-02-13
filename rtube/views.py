from rtube.models import Videos, VideoTags, VideoPhotos, Tags
from django.shortcuts import render_to_response, get_object_or_404


def index(request):
    tags = Tags.objects.all().order_by('title')
    return render_to_response('rtube/index.html', {'tags': tags})


def details(request, video_id):
    video = get_object_or_404(Videos, pk=video_id)
    video_tags = VideoTags.objects.filter(video=video)
    tags = []
    for tag in video_tags:
        tags.append(Tags.objects.get(pk=tag.tag_id))
    thumbs = VideoPhotos.objects.filter(video=video)
    return render_to_response('rtube/details.html', {'video': video, 'tags': tags, 'thumbs': thumbs})


def p(request, category):
    tag = get_object_or_404(Tags, url_string=category)
    video_tags = VideoTags.objects.filter(tag=tag)
    videos = []
    for video in video_tags:
        videos.append(Videos.objects.get(pk=video.video_id))
    return render_to_response('rtube/category.html', {'videos': videos})


def random(request):
    video = Videos.objects.order_by('?')[0]
    video_tags = VideoTags.objects.filter(video=video)
    tags = []
    for tag in video_tags:
        tags.append(Tags.objects.get(pk=tag.tag_id))
    thumbs = VideoPhotos.objects.filter(video=video)
    return render_to_response('rtube/details.html', {'video': video, 'tags': tags, 'thumbs': thumbs})
