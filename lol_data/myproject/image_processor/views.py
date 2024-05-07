from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
from .image_processing import process_image

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            # Salve a imagem em um local temporário
            with open('uploaded_image.jpg', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            # Chame a função de processamento de imagem
            result = process_image('uploaded_image.jpg')
            # Retorne o resultado como JSON
            return JsonResponse({'result': result})
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})
