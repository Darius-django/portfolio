from django.shortcuts import render,redirect
from django.http import HttpResponse
#########for forms#######
from .forms import ContactForm

def index(request):
    return render(request,'index.html')


##############Contact form##############
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            pass
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def success(request):
   return HttpResponse('Success!')
