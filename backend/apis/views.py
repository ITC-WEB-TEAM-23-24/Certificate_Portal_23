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

@permission_classes((AllowAny,))
@csrf_exempt
def posts(request):
    headers = { "Authorization": "Basic "
                + base64.b64encode(
                    f"CaDPyQf6Yf8y2529IXWZP0QXSWE3DjVzfaIZNTLu:UVZwd9alkkrgRvp8Mf0CrPTl8co02RnN0I27REwwthSFeXvn4ijT8NO3RZ39YuYx0vf8UbgOaPFo8oAAF7rvhjXDh45CgxOkfFPEmFaVM76aJsldztIDemG6AXMmgKmU".encode("utf-8")
                ).decode("utf-8"),
                "Content-Type": "application/x-www-form-urlencoded",
    }

    data = JSONParser().parse(request)
    r = requests.post('https://gymkhana.iitb.ac.in/profiles/oauth/token/', data='code='+data.get('code')+'&grant_type=authorization_code', headers=headers)
    b = requests.get('https://gymkhana.iitb.ac.in/profiles/user/api/user/?fields=first_name,last_name,roll_number', headers={'Authorization':'Bearer '+r.json()['access_token']})
    data=b.json()

    if data['last_name'] is None:
        data['last_name']=''

    user_data = {'name':data['first_name'] + ' ' + data['last_name'],'roll_number':data['roll_number']}
    return JsonResponse(user_data)


def roll_checker(roll_number, data):

    if roll_number in data['roll_number'].values:
        return True
    else :
        return False

def download_certificate(request, rollno):
    # Read data from CSV
    data = pd.read_csv((settings.BASE_DIR / "static/Book1.csv").resolve())

    # Load the image template (replace 'ksp.png' with your template file)
    template = Image.open((settings.BASE_DIR / 'static/ksp.png').resolve())

    # Initialize a drawing context on the image
    draw = ImageDraw.Draw(template)
    
    # Load a font for text rendering (replace 'font.ttf' with your font file)
    fontpath = (settings.BASE_DIR / 'static/font.ttf').resolve()
    font = ImageFont.truetype(str(fontpath), size=24)

    # Get data for the given roll_number
    certificate_data = data[data['roll_number'] == rollno].iloc[0]

    # Define text and text position
    name = certificate_data['name']
    project = certificate_data['project']
    mentor = certificate_data['mentor']
    text_position = (100, 200)  # Adjust as needed
    text_color = (255, 255, 255)  # White color (adjust as needed)

    # Draw the text on the image
    draw.text(text_position, f'Name: {name}', fill=text_color, font=font)
    draw.text((text_position[0], text_position[1] + 30), f'Project: {project}', fill=text_color, font=font)
    draw.text((text_position[0], text_position[1] + 60), f'Mentor: {mentor}', fill=text_color, font=font)

    # Create a unique filename for the certificate
    certificate_filename = f"{rollno}_certificate.png"
    certificate_path = os.path.join(settings.MEDIA_ROOT, certificate_filename)
    certificate_path_str = str(certificate_path)

    # Save the modified image to the specified path
    template.save(certificate_path_str, format='PNG')

    with open(certificate_path, 'rb') as certificate_file:
        response = HttpResponse(content=certificate_file.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{certificate_filename}"'

    os.remove(certificate_path_str)

    return response

def ksp_check(request, rollno):

    data = pd.read_csv((settings.BASE_DIR / "static/Book1.csv").resolve())
    is_mentee = roll_checker(rollno, data)
    is_mentor = roll_checker(rollno, data)
    
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

    data = pd.read_csv((settings.BASE_DIR / "static/Book1.csv").resolve())
    is_mentee = roll_checker(rollno, data)
    is_mentor = roll_checker(rollno, data)
    
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
    os.makedirs(temp_dir, exist_ok=True)

    zip_filename = f"{rollno}_ntss_certificates.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for index, certificate_data in data[data['roll_number'] == rollno].iterrows():
            template = Image.open((settings.BASE_DIR / 'static/temp_ntss.png').resolve())

            draw = ImageDraw.Draw(template)
            fontpath = (settings.BASE_DIR / 'static/font.ttf').resolve()
            
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

    os.rmdir(temp_dir)
    os.remove(zip_path)

    return response


def download_certificates_tss(request, rollno):
    data = pd.read_csv((settings.BASE_DIR / "static/tss.csv").resolve())
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_certificates')
    os.makedirs(temp_dir, exist_ok=True)

    zip_filename = f"{rollno}_tss_certificates.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for index, certificate_data in data[data['roll_number'] == rollno].iterrows():
            template = Image.open((settings.BASE_DIR / 'static/temp_tss.png').resolve())

            draw = ImageDraw.Draw(template)
            fontpath = (settings.BASE_DIR / 'static/font.ttf').resolve()
            
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

    os.rmdir(temp_dir)
    os.remove(zip_path)

    return response