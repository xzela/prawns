from django.core.management import setup_environ
from djprawn import settings
from optparse import OptionParser

setup_environ(settings)

from rtube import api

# store this shit in the database
PROVIDERS = ['rtube', 'kink']
api_urls = {
    'rtube': {
        'videos': {
            'url': 'http://api.redtube.com/?data=redtube.Videos.searchVideos',
            'params': {'category': None, 'output': 'json', 'thumbsize': 'big', 'stars': True}
        },
        'categories': {
            'url': 'http://api.redtube.com/?data=redtube.Categories.getCategoriesList',
            'params': {'output': 'json'}
        }
    },
    'kink': {
        'videos': {
            'url': '',
            'params': {}
        },
        'categories': {
            'url': '',
            'params': {}
        }
    }
}


def main():
    usage = "%prog [-a action] [-c type of content] [-s starting category]"
    version = "%prog 0.0.1a"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-a", "--action",
        action="store", type="string", dest="action",
        help="The action you wish to perform: fetch|get|list. [fetch pulls from web, get pulls from database]")
    parser.add_option('-c', "--content",
        action="store", type="string", dest="content", default=None,
        help="Which type of content you want to get: videos|categories")
    parser.add_option('-s', '--start',
        action="store", type="string", dest="starting", default=None,
        help="Starting Category you wish to start at. Try listing to see available categories")
    parser.add_option('-p', '--provider',
        action="store", type="string", dest="provider", default=None,
        help="The content Provider you wish to slurp")
    (options, args) = parser.parse_args()
    categories = []
    if options.action == "fetch":
        fetch_objects(options)
        if options.content == "categories":
            if options.provider == 'rtube':
                categories = fetch_categories()
            else:
                print "Please provider a provider or run: crab.py -a list -c providers"
        if options.content == "videos":
            categories = get_categories()
            if options.starting != None:
                if options.starting in parse_categories(categories):
                    categories = slice_category(options.starting, categories)
                else:
                    print "coud not find %s in category list. try --list" % options.starting
                    exit()
            for c in categories:
                api_urls['rtube']['videos']['params']['category'] = c.title
                # print api_urls['rtube']['videos']['params']['category']
                url = api.format_url(api_urls['rtube']['videos']['url'], api_urls['rtube']['videos']['params'])
                # print url
                # fetch api call
                json = api.fetch(url)
                pages = json['count'] / len(json['videos'])
                print pages
                for i in range(pages):
                    api_urls['rtube']['videos']['params']['page'] = i + 1
                    p_url = api.format_url(api_urls['rtube']['videos']['url'], api_urls['rtube']['videos']['params'])
                    print p_url
                    p_json = api.fetch(p_url)
                    api.insert_content(p_json, 'videos')
                    if i > 5:
                        break
                # break
            # exit()
    elif options.action == "get":
        if options.content == "categories":
            categories = get_categories()
    elif options.action == "list":
        if options.content == "categories":
            categories = get_categories()
            print "Here is a list of the known categories:"
            for c in categories:
                print c.title
        if options.content == "providers":
            print "here are the known providers:"
            for p in PROVIDERS:
                print p
        else:
            print "No content type specified. Try: categories|videos|providers"
    else:
        print "No action speficied. try --help"


def fetch_objects(options):
    if options.content == "categories":
        if options.provider != None:
            fetch_categories(options.provider)
        else:
            print "Please provider a provider or run: crab.py -a list -c providers"
    elif options.content == "videos":
        categories = get_categories()
        if options.starting != None:
            if options.starting in parse_categories(categories):
                categories = slice_category(options.starting, categories)
            else:
                print "Could not find %s in category list. run crab.py -a list -c categories to see available categories" % options.starting
                exit()
        for c in categories:
            api_urls['rtube']['videos']['params']['category'] = c.title
            # print api_urls['rtube']['videos']['params']['category']
            url = api.format_url(api_urls['rtube']['videos']['url'], api_urls['rtube']['videos']['params'])
            # print url
            # fetch api call
            json = api.fetch(url)
            pages = json['count'] / len(json['videos'])
            print pages
            for i in range(pages):
                api_urls['rtube']['videos']['params']['page'] = i + 1
                p_url = api.format_url(api_urls['rtube']['videos']['url'], api_urls['rtube']['videos']['params'])
                print p_url
                p_json = api.fetch(p_url)
                api.insert_content(p_json, 'videos')
                if i > 5:
                    break


def fetch_categories(provider="rtube"):
    if provider in PROVIDERS:
        url = api.format_url(api_urls[provider]['categories']['url'], api_urls[provider]['categories']['params'])
        json = api.fetch(url)
        api.insert_content(json, 'categories')
        return get_categories()


def parse_categories(categories):
    list_ = []
    for c in categories:
        list_.append(c.title)
    return list_


def get_categories():
    list_ = []
    for c in api.get_categories():
        list_.append(c)
    return list_


def slice_category(category, categories):
    start_from = category
    list_ = []
    temp_list = []
    for c in categories:
        temp_list.append(c.title)
    for c in temp_list[temp_list.index(start_from):]:
        list_.append(c)
    print list_
    return list_

if __name__ == "__main__":
    main()
