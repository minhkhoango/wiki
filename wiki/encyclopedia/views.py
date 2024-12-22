from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


def convert_md_to_html(title):
    markdowner = Markdown()
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries(),
    })

def entry(request, title):
    content = convert_md_to_html(title)
    if content == None:
        return render(request, 'encyclopedia/error.html', {
            "message" : "Page not found"
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            "title" : title,
            "content" : content,
        })

def search(request):
    if request.method == "POST":
        user_inp = request.POST['q']
        html_content = convert_md_to_html(user_inp)

        if html_content == None:
            entries = util.list_entries()
            possible_results = []
            for adding in entries:
                if user_inp in adding:
                    possible_results.append(adding)
            
            if not possible_results:
                return render(request, 'encyclopedia/error.html', {
                    "message" : "No results matched"
                })
            else:
                return render(request, 'encyclopedia/index.html',{
                    "title": "Did you mean...",
                    "entries" : possible_results
                })
        
        else:
            return render(request, 'encyclopedia/entry.html', {
            "title" : user_inp,
            "content" : html_content
        })

def addpage(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        entries = util.list_entries()

        if title in entries:
            return render(request, 'encyclopedia/error.html', {
                "message": f"{title} has already existed",
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('index'))
        
    return render(request, 'encyclopedia/addpage.html', {
        "title": "",
        "content": ""
    })

def random_page(request):
    title = random.choice(util.list_entries())
    file = convert_md_to_html(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "file": file
    })

def edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
    
    return render(request, 'encyclopedia/addpage.html', {
        "title": title,
        "content":content,
    })
    