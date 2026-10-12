from django.shortcuts import render

def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')
        # Здесь можно добавить сохранение в БД, отправку почты и т.д.
        message = "Спасибо, ваше сообщение отправлено!"
    return render(request, 'catalog/contacts.html', {'message': message})