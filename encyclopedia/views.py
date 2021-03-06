from django.shortcuts import render
from django import forms

from . import util
from markdown2 import Markdown
import random

markdowner = Markdown()

class Search(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'search', 'placeholder':'Search article'}))

class New_form(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'title w-50 p-3', 'placeholder':'Title'}), label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'content w-100 p-3', 'placeholder':'Type your content!'}), label='')

class Update(forms.Form):  
    textarea = forms.CharField(widget=forms.Textarea(), label='')

# def index(request):
#     return render(request, "encyclopedia/index.html", {
#         "entries": util.list_entries()
#     })

def index(request):
    query = []
    queries = util.list_entries()
    if request.method =='POST':
        form = Search(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            for i in queries:
                if title in queries:
                    article = util.get_entry(title)
                    article_html = markdowner.convert(article)
                    context = {
                        'article': article_html,
                        'title': title,
                        'form': form
                    }
                    return render(request, 'encyclopedia/article.html', context)
                if title.lower()in i.lower():
                    query.append(i)
                    context = {
                        'title': title,
                        'query': query,
                        'form' : Search() 
                    }
                    return render(request, "encyclopedia/query.html", context)
                else:
                    context={'form':Search()}
                    return render(request, 'encyclopedia/no_result.html', context)
        else:
            context={
                    "form": form
            }
            return render(request, "encyclopedia/index.html", context)
    else:
        return render(request, "encyclopedia/index.html", {
            "titles": util.list_entries(), "form":Search()
        })


def query(request, title):
    article = util.get_entry(title)
    if article is not None:
        article_html = markdowner.convert(article)
        context = {
            'form' : Search(),
            'title' : title,
            'article' : article_html
        }
        return render(request, 'encyclopedia/article.html', context)
    else:
        return render(request, 'encyclopedia/no_result.html', context)

def new_article(request):
    if request.method == 'POST':
        form = New_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            articles = util.list_entries()
            if title in articles:
                message = "Error, title already exists"
                title = 'Error'
                context = { 'form': Search(),
                            'title': title,
                            'message':message}
                return render(request, 'encyclopedia/error.html', context)
            else:
                util.save_entry(title, content)
                article = util.get_entry(title)
                article_html = markdowner.convert(article)
                # message = 'Article has been uploaded'
                context = { 'form':Search(),
                            'title':title,
                            'article':article_html}
                return render(request, 'encyclopedia/article.html', context)
        pass  
    else:
        return render(request, 'encyclopedia/save_form.html', {"form": Search(),
                "form_new":New_form()})

def update_article(request, title):
    if request.method == 'GET':
        article = util.get_entry(title)
        context = { 'form': Search(),
                    'form_update': Update(initial={'textarea': article}),
                    'title': title }
        return render(request, 'encyclopedia/update.html', context)
    else:
        form = Update(request.POST)
        if form.is_valid():
            content = form.cleaned_data['textarea']
            util.save_entry(title, content)
            article = util.get_entry(title)
            article_html = markdowner.convert(article)
            # message = "Article has been updated"
            context = { 'title': title,
                        'form': Search(),
                        'article': article_html}
            return render(request, 'encyclopedia/article.html', context)

def random_article(request):
    queries = util.list_entries()
    title = random.choice(queries)
    article = util.get_entry(title)
    article_html = markdowner.convert(article)
    context = { 'form': Search(),
                'title': title,
                'article': article_html}
    return render(request, 'encyclopedia/random.html', context)


    



    



    


