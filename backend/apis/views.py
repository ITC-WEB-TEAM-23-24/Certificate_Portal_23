from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
import base64
from rest_framework.permissions import AllowAny
import pandas as pd
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
import os
import zipfile
import shutil

@permission_classes((AllowAny,))
@csrf_exempt
def posts(request):
    headers = { "Authorization": "Basic "
                + base64.b64encode(
                    f"GrPHTL6apOjMxGVxK8JINy755G7LbZBKsEGS0ho4:lUI5RY5h0mSt2Z9EEokTmTddWGhWv4fS2UDpVTvq4CPu81L78LN0Ok88jdswXwZOo0fFq60kxbRnV5Q3xzzqnL5at1xGtnGB9GiQNj31NGoOB6BrS2OwJQJ30csRG9YA".encode("utf-8")
                ).decode("utf-8"),
                "Content-Type": "application/x-www-form-urlencoded",
    }

    data = JSONParser().parse(request)
    r = requests.post('https://gymkhana.iitb.ac.in/profiles/oauth/token/', data='code='+data.get('code')+'&grant_type=authorization_code', headers=headers)
    print('++++++++++++++++++++++++++++++')
    print(r)
    b = requests.get('https://gymkhana.iitb.ac.in/profiles/user/api/user/?fields=first_name,last_name,roll_number', headers={'Authorization':'Bearer '+r.json()['access_token']})
    data=b.json()

    if data['last_name'] is None:
        data['last_name']=''

    user_data = {'name':data['first_name'] + ' ' + data['last_name'],'roll_number':data['roll_number']}
    return JsonResponse(user_data)

def remove_files_in_folder(folder_path):
    # Ensure that the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Iterate through all items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            # Check if the item is a file
            if os.path.isfile(item_path):
                os.remove(item_path)  # Remove the file

def roll_checker(roll_number, data):
    
    data['roll_number'] = data['roll_number'].str.lower()
    if roll_number.lower() in data['roll_number'].values:
        return True
    else :
        return False

def ksp_check(request, rollno):

    data = pd.read_csv((settings.BASE_DIR / "static/Book1.csv").resolve())
    is_mentee = roll_checker(rollno, data)
    is_mentor = roll_checker(rollno, data)
    
    response_data = {
        "is_mentee": is_mentee,
        "is_mentor": is_mentor,
    }
    return JsonResponse(response_data)

def itsp_check(request, rollno):
    data = pd.read_csv((settings.BASE_DIR / "static/itsp.csv").resolve())
    is_mentee = roll_checker(rollno, data)
    is_mentor = False
    response_data = {
        "is_mentee": is_mentee,
        "is_mentor": is_mentor,
    }
    return JsonResponse(response_data)

def soc_check(request, rollno):

    data = pd.read_csv((settings.BASE_DIR / "static/Book1.csv").resolve())
    is_mentee = roll_checker(rollno, data)
    is_mentor = roll_checker(rollno, data)
    
    response_data = {
        "is_mentee": is_mentee,
        "is_mentor": is_mentor,
    }
    return JsonResponse(response_data)

def sos_check(request, rollno):

    data = pd.read_csv((settings.BASE_DIR / "static/sos.csv").resolve())
    is_mentee = False

    for roll_number in data['rollno'].values:
        if roll_number.lower() == rollno:
            is_mentee = True
            break

    is_mentor = False

    print("++++++++++++++++++++++++++"+ rollno + str(is_mentee) + "++++++++++++++++++++++++++")
    
    response_data = {
        "is_mentee": is_mentee,
        "is_mentor": is_mentor,
    }
    return JsonResponse(response_data)

def ls_check(request, rollno):

    data1 = pd.read_csv((settings.BASE_DIR / "static/ntss.csv").resolve())
    data2 = pd.read_csv((settings.BASE_DIR / "static/tss.csv").resolve())
    is_ntss = roll_checker(rollno, data1),
    is_tss = roll_checker(rollno, data2),
    response_data = {
        "in_ntss": is_ntss,
        "in_tss" : is_tss,
    }
    return JsonResponse(response_data)

def download_certificates_ntss(request, rollno):
    data = pd.read_csv((settings.BASE_DIR / "static/ntss.csv").resolve())
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_certificates')
    # os.makedirs(temp_dir, exist_ok=True)
    # os.chmod(temp_dir, 0o755)


    zip_filename = f"{rollno}_ntss_certificates.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
    data['roll_number'] = data['roll_number'].str.lower()
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for index, certificate_data in data[data['roll_number'] == rollno.lower()].iterrows():
            template = Image.open((settings.BASE_DIR / 'static/temp_ntss.png').resolve())

            draw = ImageDraw.Draw(template)
            fontpath = (settings.BASE_DIR / 'static/belleza.ttf').resolve()
            
            font1 = ImageFont.truetype(str(fontpath), size=55)
            font2 = ImageFont.truetype(str(fontpath), size=55)
            name = certificate_data['name']
            project = certificate_data['course']

            name_width, namet_height = draw.textsize(name, font=font1)
            project_width, project_height = draw.textsize(project, font=font2)
            image_width, image_height = template.size

            x1 = (image_width - name_width) // 2
            x2 = (image_width - project_width) // 2
            draw.text((x1, 650), name, fill=(0, 0, 0), font=font1)
            draw.text((x2, 900), project, fill=(0, 0, 0), font=font2)

            certificate_filename = f"{rollno}_{index + 1}_certificate.png"
            certificate_path = os.path.join(temp_dir, certificate_filename)
            template.save(certificate_path, format='PNG')
            zip_file.write(certificate_path, certificate_filename)
            os.remove(certificate_path)

    with open(zip_path, 'rb') as zip_file:
        response = HttpResponse(content=zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # os.rmdir(temp_dir)
    remove_files_in_folder(temp_dir)
    os.remove(zip_path)

    return response

def download_certificates_tss(request, rollno):
    data = pd.read_csv((settings.BASE_DIR / "static/tss.csv").resolve())
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_certificates')
    # os.makedirs(temp_dir,  exist_ok=True)
    # os.chmod(temp_dir, 0o755)

    zip_filename = f"{rollno}_tss_certificates.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
    data['roll_number'] = data['roll_number'].str.lower()
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for index, certificate_data in data[data['roll_number'] == rollno.lower()].iterrows():
            template = Image.open((settings.BASE_DIR / 'static/temp_tss.png').resolve())

            draw = ImageDraw.Draw(template)
            fontpath = (settings.BASE_DIR / 'static/belleza.ttf').resolve()
            
            font1 = ImageFont.truetype(str(fontpath), size=55)
            font2 = ImageFont.truetype(str(fontpath), size=45)
            name = certificate_data['name']
            project = certificate_data['course']

            name_width, namet_height = draw.textsize(name, font=font1)
            project_width, project_height = draw.textsize(project, font=font2)
            image_width, image_height = template.size

            x1 = (image_width - name_width) // 2
            x2 = (image_width - project_width) // 2
            draw.text((x1, 650), name, fill=(0, 0, 0), font=font1)
            draw.text((x2, 900), project, fill=(0, 0, 0), font=font2)

            certificate_filename = f"{rollno}_{index + 1}_certificate.png"
            certificate_path = os.path.join(temp_dir, certificate_filename)
            template.save(certificate_path, format='PNG')
            zip_file.write(certificate_path, certificate_filename)
            os.remove(certificate_path)

    with open(zip_path, 'rb') as zip_file:
        response = HttpResponse(content=zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # os.rmdir(temp_dir)
    remove_files_in_folder(temp_dir)
    os.remove(zip_path)
    return response

def download_certificate_itsp(request, rollno):

    data = pd.read_csv((settings.BASE_DIR / "static/itsp.csv").resolve())
    template = Image.open((settings.BASE_DIR / 'static/temp_itsp.png').resolve())
    draw = ImageDraw.Draw(template)

    fontpatha = (settings.BASE_DIR / 'static/charm.ttf').resolve()
    fontpathb = (settings.BASE_DIR / 'static/robocon.ttf').resolve()
    fonta = ImageFont.truetype(str(fontpatha), size=100)
    fontb = ImageFont.truetype(str(fontpathb), size=50)

    data['roll_number'] = data['roll_number'].str.lower()
    certificate_data = data[data['roll_number'] == rollno.lower()].iloc[0]
    name = certificate_data['name']
    team = certificate_data['team']

    name_width, name_height = draw.textsize(name, font=fonta)
    team_width, team_height = draw.textsize(team, font=fontb)
    image_width, image_height = template.size

    x1 = (image_width - name_width) // 2
    x2 = (image_width - team_width) // 2
    draw.text((x1, 600), name, fill=(57, 225, 223), font=fonta)
    draw.text((x2, 800), team, fill=(255,255,255), font=fontb)

    certificate_filename = f"{rollno}_itsp_certificate.png"
    certificate_path = os.path.join(settings.MEDIA_ROOT, certificate_filename)
    certificate_path_str = str(certificate_path)

    template.save(certificate_path_str, format='PNG')

    with open(certificate_path, 'rb') as certificate_file:
        response = HttpResponse(content=certificate_file.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{certificate_filename}"'
    os.remove(certificate_path_str)

    return response

def download_certificate_sos(request, rollno):

    data = pd.read_csv((settings.BASE_DIR / "static/sos.csv").resolve())
    template = Image.open((settings.BASE_DIR / 'static/sos.png').resolve())
    draw = ImageDraw.Draw(template)

    fontpatha = (settings.BASE_DIR / 'static/charm.ttf').resolve()
    fontpathb = (settings.BASE_DIR / 'static/robocon.ttf').resolve()
    fonta = ImageFont.truetype(str(fontpatha), size=200)
    fontb = ImageFont.truetype(str(fontpathb), size=150)

    certificate_data = data[data['rollno'].str.lower() == rollno.lower()].iloc[0]
    name = certificate_data['name']
    team = certificate_data['topic']

    name_width, name_height = draw.textsize(name, font=fonta)
    team_width, team_height = draw.textsize(team, font=fontb)
    image_width, image_height = template.size

    x1 = (image_width - name_width) // 2
    x2 = (image_width - team_width) // 2
    draw.text((x1, 2000), name, fill=(0,0,0), font=fonta)
    draw.text((x2, 2650), team, fill=(0,0,0), font=fontb)

    certificate_filename = f"{rollno}_itsp_certificate.png"
    certificate_path = os.path.join(settings.MEDIA_ROOT, certificate_filename)
    certificate_path_str = str(certificate_path)

    template.save(certificate_path_str, format='PNG')

    with open(certificate_path, 'rb') as certificate_file:
        response = HttpResponse(content=certificate_file.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{certificate_filename}"'
    os.remove(certificate_path_str)

    return response

