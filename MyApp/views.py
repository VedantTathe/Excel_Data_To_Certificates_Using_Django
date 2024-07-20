from django.shortcuts import render
from .forms import ExcelCertifInputForm
from .models import ExcelCertifInput

import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound


def generate_certificates(font_size, y_position, output_pdf, output_folder, df, template, template_width, template_height, column_name):
    font_path = "times.ttf"  # Update to your font path
    font = ImageFont.truetype(font_path, font_size)

    c = canvas.Canvas(output_pdf, pagesize=landscape((template_width, template_height)))

    for index, row in df.iterrows():
        name = row[column_name]

        certificate = template.copy()
        draw = ImageDraw.Draw(certificate)

        # Calculate text size using textbbox
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        # text_height = text_bbox[3] - text_bbox[1]

        # Calculate center position
        x_position = (template_width - text_width) / 2
        # y_position = (template_height - text_height) / 2

        draw.text((x_position, y_position), name, font=font, fill="black")

        temp_image_path = os.path.join(output_folder, f"{name}_temp.png")
        certificate.save(temp_image_path)

        c.drawImage(temp_image_path, 0, 0, width=template_width, height=template_height)
        c.showPage()

        os.remove(temp_image_path)

    c.save()

    print("All certificates have been generated into a single PDF successfully!")


def select_text_position(request):
    success = False
    if request.method == 'POST':
        font_size = request.POST.get('font_size')
        x_position = request.POST.get('x_position')
        y_position = request.POST.get('y_position')
        excelcertifinput_id = int(request.POST.get('excelcertifinput_id'))

        excelcertifinput = ExcelCertifInput.objects.get(id=excelcertifinput_id)
        excel_file = excelcertifinput.excelfile.path
        template_image = excelcertifinput.certificateimg.path
        output_folder = os.path.join(settings.STATIC_DIR, 'pdfofcertificates')
        output_pdf = os.path.join(output_folder, f'all_certificates{excelcertifinput_id}.pdf')

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        df = pd.read_excel(excel_file)
        template = Image.open(template_image)
        template_width, template_height = template.size

        generate_certificates(int(font_size), int(y_position), output_pdf, output_folder, df, template, template_width, template_height, excelcertifinput.column_name)

        success = 'All certificates have been generated and merged into a single PDF successfully..!'
        return render(request, 'MyApp/select_text_position.html', {'success': success, 'excelcertifinput_id': excelcertifinput_id})

    else:
        return render(request, 'MyApp/select_text_position.html', {
            'template_image': settings.MEDIA_URL + request.GET.get('template_image'),
            'excelcertifinput_id': request.GET.get('excelcertifinput_id'),
            'success': success
        })


def index(request):
    try:
        success = False
        if request.method == 'POST':
            form = ExcelCertifInputForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                success = True
                excelcertifinput = form.instance

                df = pd.read_excel(excelcertifinput.excelfile.path)
                first_row_name = "Sample Name"
                if not df.empty:
                    # excelcertinput = ExcelCertifInput.objects.get(id=excelcertifinput.id)
                    first_row_name = df.iloc[0][excelcertifinput.column_name]

                return render(request, 'MyApp/select_text_position.html', {
                    'template_image': excelcertifinput.certificateimg.url,
                    'excelcertifinput_id': excelcertifinput.id,
                    'first_row_name': first_row_name
                })
            else:
                return render(request, 'MyApp/index.html', {'form': form, 'success': 'Invalid Input Given..!'})
        else:
            form = ExcelCertifInputForm()

        return render(request, 'MyApp/index.html', {'form': form, 'success': success})
    except KeyError as e:
        return render(request, 'MyApp/index.html', {'form': form, 'success': 'Key Error: Please Enter Valid Column Name'})



def download_pdf(request, excelcertifinput_id):
    pdf_path = os.path.join(settings.BASE_DIR, 'static', 'pdfofcertificates', f'all_certificates{excelcertifinput_id}.pdf')
    if os.path.exists(pdf_path):
        response = FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename='all_certificates.pdf')
        return response
    else:
        return HttpResponseNotFound("PDF file not found.")
