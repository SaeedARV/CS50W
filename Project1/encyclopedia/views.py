from logging import PlaceHolder
from logging.config import valid_ident
from multiprocessing.sharedctypes import Value
from turtle import title
from django.shortcuts import render
from markdown2 import markdown
from django import forms

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    markDown = forms.CharField(widget=forms.Textarea(), label="Markdown")

class EditPageForm(forms.Form):
    markDown = forms.CharField(widget=forms.Textarea(), label="Markdown")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getContent(request, title):
    content = util.get_entry(title)

    if content != None:
        content = markdown(content)
        return render(request, "encyclopedia/entryPage.html", {
            "title": title,
            "content": content
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "error": 'The page"' + title + '"does not exist!'
        })

def search(request):
    title = request.GET.get('q')
    content = util.get_entry(title)

    if content != None:
        content = markdown(content)
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

    
def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        entries = util.list_entries()

        if form.is_valid():
          title = form.cleaned_data['title']
          markDown = form.cleaned_data['markDown']

        if title in entries:
            return render(request, "encyclopedia/error.html", {
                "error": 'The page"' + title + '"already exist!'
            })
        else:
            util.save_entry(title, markDown)
            return render(request, "encyclopedia/entryPage.html", {
                "title": title,
                "content": markdown(markDown)
            })
    else:
        return render(request, "encyclopedia/newPage.html", {
            "form": NewPageForm()
        })

def editPage(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        entries = util.list_entries()

        if form.is_valid():
            markDown = form.cleaned_data['markDown']
            util.save_entry(title, markDown)
            return render(request, "encyclopedia/entryPage.html", {
                "title": title,
                "content": markdown(markDown)
            })

    else:
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "form": EditPageForm(initial={'markDown':util.get_entry(title)})
        })