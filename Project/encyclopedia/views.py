from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getContent(request, title):
    content = util.get_entry(title)

    if content == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    
    else:
        return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": content
        })


