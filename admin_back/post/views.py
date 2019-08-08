from django.shortcuts import render, redirect
from ..steam.models import Steam, Steam_Data
from django.contrib import messages
from .models import content as post_content
from ..AdminPackage.AdminController import CheckLogin

# Create your views here.

def post_edit(request, post_id):
    params = {}
    
    checklogin = CheckLogin(request)
    print(checklogin)
    if checklogin == True:

        email = ""

        try:
            get_post = post_content.objects.get(create_by=email, id=post_id)

            if get_post:
                params['edit'] = get_post
                

        except:
            redirect("https://www.google.com")
    
    return render(request, "admin_html/post.html", params)

    


def post_delete(request, post_id):

    checklogin = CheckLogin(request)
    print(checklogin)
    if checklogin == True:

        email = ""

        try:
            get_post = post_content.objects.get(create_by=email, id=post_id)
            delete = get_post.delete()
            
            if delete:
                messages.success(request, "Post deleted")

        except:
            messages.success(request, "An error occured please try again later.", extra_tags="danger")

    


    params = {}
    params['posts'] = post_content.objects.all()



    
    return render(request, "admin_html/view_post.html", params)



def post_view(request):

    params = {}
    params['posts'] = post_content.objects.all()



    
    return render(request, "admin_html/view_post.html", params)

def post_add(request):

    params = {}
    get_all_steam = Steam.objects.all()
    params['steam_c'] = get_all_steam

    if request.method=="POST":
        
        title = request.POST['title']
        desc = request.POST['desc']
        content = request.POST['content']
        sub_category = request.POST['sub_category']
        second_sub_category = request.POST['second_sub_category']
        category = request.POST['category']
        scp = True
        Program = "B-Tech"
        branch = "CSE"
        sem = "3"
        create_by = ""
        try:

            if request.POST['publish']=='':
                status = "Active"
                status_msg = "Post has been succesfully posted"
        except:
            pass


        try:
             if request.POST['draft']=='':
                     status = "Draft"
                     status_msg = "Post has been succesfully Drafted"

        except:
            pass


        if title!='' and desc!='' and content!='' and category!='' and sub_category!='':

            insert = post_content.objects.create(
                     create_by = create_by,
                     status = status,
                     title = title,
                     description = desc,
                     categoryOne = category,
                     categoryTwo = sub_category,
                     categoryThree = second_sub_category,
                     categoryFour = "",
                     isSCP = scp,
                     SCP_program = Program,
                     SCP_branch = branch,
                     SCP_semester = sem,
                     
          )

            if insert:
                 messages.success(request, status_msg)
            
        else:
            messages.error(request, "All fields are mandatory.", extra_tags="danger")

               
            


    
    
    return render(request, "admin_html/post.html", params)

    