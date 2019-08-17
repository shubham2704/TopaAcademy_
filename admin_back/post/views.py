from django.shortcuts import render, redirect, HttpResponse
from ..steam.models import Steam, Steam_Data
from django.contrib import messages
from .models import content as post_content, attachment as post_att
from ..AdminPackage.AdminController import CheckLogin
from ..branch.models import branch_degree, branchs
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import json
import random
import string
import os

# Create your views here.

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


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
            'branch':False,
            'type_a':"Semester",
            'semester' : {}

        }
        if steam == 'l':
            branch_deg = branch_degree.objects.all()
            params['get_degree'] = branch_deg
            
            params['steam'] = True
           

            

            
        if branch != 'no':
            params['get_branch'] = branchs.objects.filter(degree_name=branch)
            params['degree_selected'] = branch
            get_degree = branch_degree.objects.get(degree_name=branch)
            sem_list = []
            if get_degree.semester == "Yearly":
                params['type_a'] = "Year"
                
                for rb in range(1 ,int(get_degree.duration) + 1):
                    sem_list.append(rb)
                    
            else:
                for rb in range(1, int(get_degree.semester) + 1):
                    sem_list.append(rb)



            params['branch'] = True
            params['semseter'] = sem_list

            print(params)
        
        
        
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
    params = {
        "edit_b" : True
    }
    get_all_steam = Steam.objects.all()
    params['steam_c'] = get_all_steam
    
    checklogin = CheckLogin(request)
    print(checklogin)
    if checklogin == True:

        email = ""

        try:

            get_session = request.GET['ses']
            #print(get_session)
        

            try:
                get_post = post_content.objects.get(create_by=email, id=post_id, creation_session=get_session)
                attachmentt = post_att.objects.filter(creation_session=get_session, status="Active")

                if get_post:
                    params['edit'] = get_post
                    params['attachment'] = attachmentt
                    
                    print(get_post)
                    
            
            except:
                return redirect("/admin-panel/post?er_cd=425")

        except:
            return redirect("/admin-panel/post/")

    
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
def upload_file(request, ses_id):
    
    

    try:
        if request.method == 'POST' and request.FILES['file']:
            myfile = request.FILES['file']
            ran = randomString(10)
            support_ext = ['jpg', 'jpeg']
            
            folder = "templates/media/upload_attachment/"
            SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
            full_filename = os.path.join(SITE_ROOT, folder, ran + myfile.name)
            ext = myfile.name.split(".")[-1]

            if ext.lower() in support_ext:
                
                fout = open(full_filename, 'wb+')
                file_content = ContentFile( myfile.read())

                


                for chunk in file_content.chunks():
                        fout.write(chunk)
                fout.close()

                filesize= os.path.getsize(full_filename)
                
                if filesize <= 5242880:
                

                    insert = post_att.objects.create(
                        status = "Active",
                        creation_session = ses_id,
                        filename = ran + myfile.name,
                        upload = ran + myfile.name,
                        actual_filename = myfile.name,
                        extension = ext
                    
                    )
                    if insert:
                        
                        status = 200
                    else:
                        status = 499
                else:
                    status = 487

            else:
                status = 488
        else:
            status = 499

        
    except:
        status = 499

    return HttpResponse(request, "", status)

def post_add(request):

    params = {}
    get_all_steam = Steam.objects.all()
    params['steam_c'] = get_all_steam

    try:
        get_session = request.GET['ses']
        params['session_post'] = get_session

        if request.method=="POST":
            
            title = request.POST['title']
            desc = request.POST['desc']
            content = request.POST['content']
            
            sub_category = request.POST['sub_category']
            second_sub_category = request.POST['second_sub_category']
            category = request.POST['category']
            print(category)

            try:
                degree = Steam.objects.get(steam_link_id = category)
                category = degree.steam_name
                print(degree)
            except:
                category=""

            scp = False
            try:

                if request.POST['isSCT'] == "on":
                    scp = True
            except:
                pass
            Program = request.POST['pr']
            branch = request.POST['br']
            sem = request.POST['sm']
            create_by = ""
            try:

                if request.POST['publish']=='':
                    status = "Published"
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
                start_insert = True
                if scp == True:

                    if Program=='' or branch=='' or sem=='':

                        start_insert = False
                        messages.error(request, "All fields are mandatory.", extra_tags="danger")
                    
                if start_insert == True:
                    insert = post_content.objects.create(
                        create_by = create_by,
                        creation_session = get_session,
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
    except:

        sess = randomString(10)

        return redirect("/admin-panel/post/add?ses="+sess)
        
               
            


    
    
    return render(request, "admin_html/post.html", params)

    