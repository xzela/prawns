# Create your views here.
from rtube.models import Categories, Videos, VideoTags, VideoPhotos, Tags
import urllib, urllib2, json
from django.db import IntegrityError
from django.db.models import Count
from datetime import datetime
import re
import os


def fetch(url):
    request = urllib2.urlopen(url)
    # j = simplejson.dumps(request.read())
    # data = json.load(j)
    data = json.loads(request.read())
    # insert_content(data)
    # return HttpResponse(data)
    # return render_to_response('papi/open_api.html', {'data': data})
    return data


def format_url(url, params):
    url_string = url + '&' + urllib.urlencode(params)
    return url_string


def insert_content(data, content_type):
    if content_type == 'videos':
        for d in data['videos']:
            video = insert_video(d['video'])
            # print video.redtube_id
            if 'tags' in d['video']:
                for tag in d['video']['tags']:
                    tag = {'title': tag['tag_name']}
                    tag_object = insert_video_tag(tag)
                    assign_video_tag(tag_object, video)
                # insert_video_tags(d['video']['tags'])
            photos = insert_video_photos(video, d['video']['thumbs'])
    elif content_type == 'categories':
        for d in data['categories']:
            category = insert_category(d)
    return data


def insert_video(video):
    v = None
    try:
        pub = video['publish_date']
        if pub == False:
            pub = datetime.now()
        v = Videos(
            redtube_id=video['video_id'],
            url=video['url'],
            status='active',
            title=video['title'],
            rating=video['rating'],
            number_of_ratings=video['ratings'],
            publish_date=pub,
            duration=video['duration'],
            number_of_views=video['views'])
        v.save()
    except IntegrityError, e:
        v = Videos.objects.get(redtube_id=video['video_id'])
        # print e.message
    return v


# def insert_video_tags(video, tags):
#     t = None
#     for tag in tags:
#         try:
#             t = VideoTags(video=video, title=tag['tag_name'])
#             t.save()
#         except IntegrityError, e:
#             t = VideoTags.objects.get(video=video, title=tag['tag_name'])
#             # print e.message
#     return t


def insert_video_photos(video, thumbs):
    p = None
    for thumb in thumbs:
        try:
            p = VideoPhotos(
                video=video,
                url=thumb['src'],
                filename=os.path.basename(thumb['src']),
                size=thumb['size'],
                width=thumb['width'],
                height=thumb['height'])
            p.save()
        except IntegrityError:
            p = VideoPhotos.objects.get(video=video, filename=os.path.basename(thumb['src']))
            # print e.message
    return p


def insert_category(category):
    c = None
    try:
        c = Categories(
            title=category['category'],
            content_type='all'
        )
        c.save()
    except IntegrityError:
        c = Categories.objects.get(title=category['category'])
    return c


def fetch_grouped_video_tags():
    tags = VideoTags.objects.values('title').extra({'count': 'count(title)'}).annotate(count=Count('id'))
    return tags


def assign_video_tag(tag, video):
    try:
        VideoTags(tag=tag, video=video).save()
    except IntegrityError:
        return None
    return None


def insert_video_tag(tag):
    t = None
    url_string = re.sub(r'([^\s\w]|_)+', '', tag['title']).replace(" ", "-").lower()
    # print url_string
    safe_tag = ''.join(e for e in tag['title'].lower() if e.isalpha())
    try:
        t = Tags(title=safe_tag, url_string=url_string, original=tag['title'])
        t.save()
    except IntegrityError:
        t = Tags.objects.get(title=safe_tag)
    return t


def insert_video_tags(tags):
    t = None
    for tag in tags:
        url_string = re.sub(r'([^\s\w]|_)+', '', tag['title']).replace(" ", "-").lower()
        print url_string
        safe_tag = ''.join(e for e in tag['title'].lower() if e.isalpha())
        try:
            t = Tags(title=safe_tag, url_string=url_string, original=tag['title'])
            t.save()
        except IntegrityError:
            t = Tags.objects.get(title=safe_tag)
    return t


def get_categories():
    categories = Categories.objects.all()
    return categories
