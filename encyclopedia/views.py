from django.shortcuts import render
from django import forms

from . import util
from markdown2 import Markdown

markdowner = Markdown()

class Search(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'search', 'placeholder':'Search'}))

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
                    return render(request, 'encyclopedia/result.html', context)
                if title.lower()in i.lower():
                    query.append(i)
                    context = {
                        'query': query,
                        'form' : Search() 
                    }
            return render(request, "encyclopedia/query.html", context)
        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
        })

  

