from logging.config import valid_ident
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getContent(request, title):
    content = util.get_entry(title)

    if content != None:
        return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": content
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

def search(request):
    title = request.GET.get('q')
    content = util.get_entry(title)

    if content != None:
        return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": content
        })
    else:
        subStrings = []
        entries = util.list_entries()

        for entry in entries:
            if title.upper() in entry.upper():
                subStrings.append(entry)
        return render(request, "encyclopedia/search.html", {
            "title": title,
            "subStrings": subStrings
        })

    

