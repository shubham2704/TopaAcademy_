from django.shortcuts import render, redirect, HttpResponse
from ..steam.models import Steam, Steam_Data
from django.contrib import messages
from .models import content as post_content
from ..AdminPackage.AdminController import CheckLogin
from ..branch.models import branch_degree, branchs
import json

# Create your views here.


def steam_dual_ajax(request,id, name):
    params = {}
    params['steam_id']= id
    params['dualevel'] = True
    params['name'] = name

    get_steam_data = Steam_Data.objects.get(id=id)
    get_data = get_steam_data.steam_data_json
    get_level = get_steam_data.multilevel_data
    decode_json = json.loads(get_data)
    params['json'] = decode_json

    for looping_steam_data in decode_json:
        val = decode_json[looping_steam_data]['level_name']
        print(val, name)
        
        if val == name:
            print("dss")
            params['dual_data'] = decode_json[looping_steam_data]['data']
        
        

    print(params['dual_data'])
    return render(request, "admin_html/ajax_html/steam_post_ajax.html", params)  


def sct_ajax(request, sct_bool, steam, branch):

    if sct_bool == 'true':
        params = {

            'steam': False,
            'branch':False

        }
        if steam == 'l':
            params['get_degree'] = branch_degree.objects.all()
            print(params['get_degree'])
            params['steam'] = True
            
        if branch != 'no':
            params['get_branch'] = branchs.objects.filter(degree_name=branch)
            params['degree_selected'] = branch
            print(branch)
            params['branch'] = True
            
        
        
        return render(request, "admin_html/ajax_html/post_sct.html", params)   
    else:
        return HttpResponse("")


def ajax_steam(request,sid):
    params = {}
    params['steam_id']= sid

    get_steam_data = Steam_Data.objects.get(id=sid)
    get_data = get_steam_data.steam_data_json
    get_level = get_steam_data.multilevel_data
    decode_json = json.loads(get_data)

    if get_level == 'Single Level':
        params['single'] = True
        params['json'] = decode_json
    if get_level == 'Double Level':
        params['multiple'] = True   
        params['json'] = decode_json


    return render(request, "admin_html/ajax_html/steam_post_ajax.html", params)   

def post_edit(request, post_id):
    params = {}
    get_all_steam = Steam.objects.all()
    params['steam_c'] = get_all_steam
    
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
        print(content)
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
                     content=content,
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

    