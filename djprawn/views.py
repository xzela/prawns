from django.shortcuts import render_to_response


def index(request):
    return render_to_response('static/index.html')


def doubleu():
    return "w"
