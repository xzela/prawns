# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from rtube.models import Category, Video, Tag, VideoPhoto
import urllib, urllib2, json, simplejson
from django.db import IntegrityError


def open_api(request):
    params = {'category': 'shemale', 'output': 'json', 'thumbsize': 'none', 'stars': True}
    url_string = 'http://api.redtube.com/?data=redtube.Videos.searchVideos' + '&' + urllib.urlencode(params)
    request = urllib2.urlopen(url_string)
    # j = simplejson.dumps(request.read())
    # data = json.load(j)
    data = json.loads(request.read())
    parse_json(data)
    # return HttpResponse(data)
    return render_to_response('papi/open_api.html', {'data': data})
    # return data


def insert_video(video):
    v = None
    try:
        v = Video(
            redtube_id=video['video_id'],
            url=video['url'],
            status='active',
            title=video['title'],
            rating=video['rating'],
            number_of_ratings=video['ratings'],
            publish_date=video['publish_date'],
            duration=video['duration'],
            number_of_views=video['views'])
        v.save()
    except IntegrityError, e:
        v = Video.objects.get(redtube_id=video['video_id'])
        print e.message
    return v


def parse_json(data):
    for k in data['videos']:
        v = insert_video(k['video'])
        t = insert_tag(v, k['video']['tags'])
    return True


def insert_tag(video, tags):
    for tag in tags:
        t = None
        try:
            t = Tag(video=video, title=tag['tag_name'])
            t.save()
        except IntegrityError, e:
            t = Tag.objects.get(video=video, title=tag['tag_name'])
            print e.message
    return t
