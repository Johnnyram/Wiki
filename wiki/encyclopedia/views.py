from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import wikiForm
from .forms import titleForm
from .forms import bodyForm
from .forms import editForm
import random
import markdown

from . import util


def index(request):
	return render(request, "encyclopedia/index.html",{
		"entries": util.list_entries()
	})

def wiki(request, title):
	lis=util.list_entries()
	if title in lis:
		return HttpResponse(markdown.markdown(util.get_entry(title)))
	else:
		return HttpResponse(f'{title} search is not found,please try again.')
def click_entry(request):
	list_entry=util.list_entries()
	for entry in list_entry:	
		if str(entry) in request.POST:
			name = str(entry)
			return HttpResponse(markdown.markdown(util.get_entry(name)))
	return render(request, "encyclopedia/index.html",{    
		"name": name
	})


def open(request):
	entries = util.list_entries()
	substring_entries = []
	if request.method == "POST":
		forms = wikiForm(request.POST)
		if forms.is_valid():
			wiki = forms.cleaned_data["wiki"]
			if wiki in entries:
				return HttpResponse(markdown.markdown(util.get_entry(wiki)))
			else:
				for entry in entries:
					if wiki in entry:
						substring_entries.append(entry)
				return render(request,'encyclopedia/Substring entries.html',{
					"substring_entries": substring_entries
				})
		else:
			forms = wikiForm()
		return render(request,'encyclopedia/index.html',{
			'forms': wikiForm()
		})
def new_entry(request):
	entries=util.list_entries()
	if request.method == "POST":
		title = titleForm(request.POST)
		body = bodyForm(request.POST)
		if title.is_valid() and body.is_valid():
			if title in entries:
				return HttpResponse(f'Their already is a file under the title {title}.')
			else:
				title = title.cleaned_data["title"]
				body = body.cleaned_data["body"]
				util.save_entry(title, body)
				return HttpResponse(markdown.markdown(util.get_entry(title)))
		else:
			title = titleForm()
			body = bodyForm()
	return render(request,'encyclopedia/new page.html',{
		'title': titleForm(),
		'body': bodyForm() 
	})
def random_page(request):
	entries=util.list_entries()
	rand=random.randint(0,len(entries)-1)
	random_entry = entries[rand]
	return HttpResponse(markdown.markdown(util.get_entry(random_entry)))

#
def edit(request, title):
	if request.method == 'POST':
		util.save_entry(title, request.POST['body'])
		return HttpResponse(markdown.markdown(util.get_entry(title)))
	else:
		body = util.get_entry(title)
		form = editForm(request.POST or None, initial={'body':body})
		return render(request, "encyclopedia/markdown editor.html", {
			"title": title,
			"body": body,
			"form": form
		})