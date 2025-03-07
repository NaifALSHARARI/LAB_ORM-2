from django.shortcuts import render ,redirect
from django.http import HttpRequest
from .models import Blog
# Create your views here.


def add_blogs_view(request:HttpRequest):
    try:
        if request.method == "POST":
            new_blogs = Blog(title=request.POST["title"], content=request.POST["content"], is_published = request.POST["is_published"], published_at = request.POST["published_at"], category=request.POST["category"],poster=request.FILES['poster'])
            new_blogs.save()
            return redirect("blogs:show_blogs_view")

        
        return render(request,"blogs/add.html", {"categories" : Blog.categories})
    except Exception as e:
        return redirect("blogs:not_found_view")
        


def show_blogs_view(request:HttpRequest):
    
    blogs=Blog.objects.all()
    
    return render(request,"blogs/show_blogs.html", {"blogs" : blogs})

def not_found_view(request:HttpRequest):
        return render(request,"blogs/not_found.html")

def blog_detail_view(request:HttpRequest, blog_id):
    
    try :
        blog = Blog.objects.get(id=blog_id)
        return render(request,"blogs/detail.html" , {"blog":blog})
    except Exception as e:
        return redirect("blogs:not_found_view")
    
def blog_update_view(request:HttpRequest, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        if request.method == "POST":
                blog.title = request.POST["title"]
                blog.content = request.POST["content"]
                blog.is_published = request.POST["is_published"]
                blog.published_at =request.POST["published_at"]
                blog.category = request.POST["category"]
                blog.poster = request.FILES["poster"]
                blog.save()
            
                return redirect('blogs:blog_detail_view',blog_id=blog_id)
        return render(request,"blogs/update.html", {"blog" : blog, "categories"  : Blog.categories})
    except Exception as e :
        return redirect("blogs:not_found_view")



def blog_delete_view(request:HttpRequest, blog_id):
        blog = Blog.objects.get(id=blog_id)
        blog.delete()
        return redirect("blogs:show_blogs_view")
        

    
def search_results_view(request: HttpRequest):

    if "search" in request.GET:
        keyword = request.GET["search"]
        blogs = Blog.objects.filter(title__contains=keyword)
    else:
        blogs = Blog.objects.all()


    return render(request, "blogs/search.html", {"blogs" : blogs}) 

def blogs_home_view_cat(request: HttpRequest, cat):

    
    blogs = Blog.objects.filter(category=cat)

    

    blogs_count = blogs.count()

    return render(request, "blogs/show_blogs.html", {"blogs" : blogs, "blogs_count" : blogs_count})
