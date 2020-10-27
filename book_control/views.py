from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
import book_control.models as models
import datetime

def index(request):
    cursor = models.mySql_work()
    articles = cursor.Select()
    print("articles",type(articles[0]),articles[0])
    string = str( type(articles))
    return HttpResponse(string)

def list_show(request):
    cursor = models.mySql_work()
    title,Author ="",""
    if request.method == "POST":  
        title = request.POST["title"] 
        Author = request.POST["Author"]
    # articles = cursor.Select()
    print(title,Author)
    onepagelist = cursor.Select(title,Author)
    for x in onepagelist:
        x["publishedDate"] = str(x["publishedDate"])
    return render(request, 'list.html',{"onepagelist":onepagelist})

def addpage(request):
    cursor = models.mySql_work()
    ISBN = ""
    if request.method == "POST":  
        ISBN = request.POST["ISBN"]
        cursor.addBook(ISBN)
    print(ISBN)

    return render(request, 'add.html')

def remove(request):
    print(request)
    print("=============================")
    if request.method == "POST":  
        print("=============================")
    if request.GET:
        ISBN=request.GET['ISBN']
        cursor = models.mySql_work()
        cursor.delBook(ISBN)

    return HttpResponseRedirect("/book/list")

