from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import ContactForm,ScrapDataForm
from .models import Post,Comment
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import PermissionDenied
#------------srap imports--------------
import pandas as pd
from bs4 import BeautifulSoup
#-----video downloader imports--------
from pytube import YouTube
from django.conf import settings
#---converter block here-----------
import json
import os
import re
#
from .models import ScrapData
#
import pyshorteners
from .models import URL


def index(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            messages.error(request, 'Užpildykite visus laukus!')
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})

def success(request):
   return render(request, 'sucess.html')

def blog(request):
   return render(request, 'blog.html')

#---------BLOG SIDE HERE-------------
class PostList(generic.ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.order_by('-created_on')

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog.html'

#----------coments block here--------------------------------------
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(active=True).order_by('created_on')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_body = request.POST.get('comment')

        if name and email and comment_body:  # Check if all fields are filled
            comment = Comment(post=post, name=name, email=email, body=comment_body)
            comment.save()
            messages.info(request, 'Sėkmingai parašėte komentarą!')
            return redirect('blog')
        else:
            messages.error(request, 'Užpildykite visus laukus!')

    return render(request, 'blog.html', {'post': post, 'comments': comments})
#-------SEARCH BLOCK HERE-------------------------------------------------------------------------
def search(request):
    query = request.GET.get('query')
    search_results = Post.objects.filter(Q(body__icontains=query) | Q(author__icontains=query))
    return render(request, 'blog.html', {'posts': search_results, 'query': query})
#-------scrap BLOCK HERE-------------------------------------------------------------------------
import requests

def my_view(request):
    url = "https://www.lrytas.lt/"
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    # Ištraukiame informaciją iš HTML puslapio
    data = []
    for link in soup.find_all('a'):
        link_url = link.get('href')
        link_title = link.text.strip()

        # Tikriname, ar nuoroda yra tinkama, turime pavadinimą (ne skaičius), ir URL turi fragmentą "https://"
        if link_url and link_title and not link_title.isdigit() and "https://" in link_url:
            data.append({'url': link_url, 'title': link_title})

    # Ištriname eilutes, kur 'title' stulpelyje yra fragmentas '00:17:49' (arba bet kokie skaičiai)
    data = [item for item in data if not re.match(r'^\d{2}:\d{2}:\d{2}$', item['title'])]

    # Įrašome rezultatus į duomenų bazę
    for item in data:
        ScrapData.objects.create(title=item['title'], url=item['url'])

    # Sukuriame duomenų rėmelį (DataFrame)
    df = pd.DataFrame(data, columns=['url', 'title'])

    # Pass the DataFrame to the template as context
    context = {'df': df}

    if request.method == 'POST':
        form = ScrapDataForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ScrapDataForm()

    return render(request, 'scrap.html', {'df': df, 'form': form})

#-------video downloader block--------------------
def display_available_formats(streams):
    available_formats = []
    for i, stream in enumerate(streams):
        available_formats.append(f"{i + 1}. {stream.resolution} - {stream.mime_type}")
    return available_formats

def video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')

        try:
            # Create a YouTube object with the video URL
            youtube = YouTube(video_url)

            # Get video information
            author = youtube.author
            title = youtube.title
            views = youtube.views
            length = youtube.length
            rating = youtube.rating

            # Get the highest resolution stream
            stream = youtube.streams.get_highest_resolution()

            # Set the destination path to save the downloaded file
            filename = f"{title}.mp4"
            destination_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Download the video to the specified path
            stream.download(output_path=settings.MEDIA_ROOT, filename=filename)

            # Check if the file exists in the destination path
            if os.path.exists(destination_path):
                success_message = "Video downloaded successfully."
                video_info = {
                    'author': author,
                    'title': title,
                    'views': views,
                    'length': length,
                    'rating': rating,
                    'success_message': success_message,
                    'file_path': os.path.join(settings.MEDIA_URL, filename),
                }
                return render(request, 'video.html', video_info)
            else:
                error_message = "Failed to download the video."
                video_info = {'error_message': error_message}
                return render(request, 'video.html', video_info)

        except Exception as e:
            error_message = "Error: " + str(e)
            video_info = {'error_message': error_message}
            return render(request, 'video.html', video_info)

    return render(request, 'video.html')
#https://www.youtube.com/watch?v=DnGdoEa1tPg
#-------short block here--------------------
# def short(request):
#     return render(request, 'short.html')
def shorten_url(url):
    try:
        # Create a Shortener object
        shortener = pyshorteners.Shortener()

        # Shorten the URL
        shortened_url = shortener.tinyurl.short(url)

        return shortened_url

    except Exception as e:
        print("Error:", str(e))

def short(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        # Call the shorten_url function to shorten the URL
        shortened_url = shorten_url(url)

        # Save the original URL and shortened URL to the database
        url_object = URL(original_url=url, shortened_url=shortened_url)
        url_object.save()

        # Pass the shortened URL and original URL to the template
        return render(request, 'short.html', {'shortened_url': shortened_url, 'original_url': url})

    return render(request, 'short.html')

#------------------multiply shortener------------------
def shorten_multiple(request):
    if request.method == 'POST':
        url_inputs = request.POST.getlist('url_input')  # Gauti sąrašą URL iš formos

        # Gauti įkeltą failą
        file = request.FILES.get('file_input')
        if file:
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)

            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Skaityti URL iš failo
            with open(file_path, 'r') as file:
                url_list = file.read().split('\n')
                url_inputs.extend(url_list)

            # Ištrinti failą po naudojimo
            os.remove(file_path)

        # Sutrumpinkite URL ir atlikite kitus veiksmus...
        shortened_urls = []
        for url in url_inputs:
            shortened_url = shorten_url(url)  # Jūsų URL sutrumpinimo logika
            shortened_urls.append(shortened_url)
            # Įrašyti į duomenų bazę
            url_obj = URL(original_url=url, shortened_url=shortened_url)
            url_obj.save()

        return render(request, 'short.html', {'url_inputs': url_inputs, 'shortened_urls': shortened_urls})

    return render(request, 'short.html')
#-----quiz block here-------------
from django.shortcuts import render
from django.views.generic import ListView
from .models import Question

def quiz(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'quiz.html', context)

def quiz_results(request):
    if request.method == 'POST':
        questions = Question.objects.all()
        total = len(questions)
        score = 0
        for question in questions:
            selected_option = request.POST.get(f"question_{question.id}")
            if selected_option == question.ans:
                score += 1
        percent = (score / total) * 100
        context = {
            'score': score,
            'correct': score,
            'total': total,
            'percent': percent,
            'show_results': True
        }
        return render(request, 'quiz_results.html', context)
    raise PermissionDenied

class QuestionListView(ListView):
    model = Question
    template_name = 'quiz.html'
    context_object_name = 'questions'

#----------------converter block herre------------------
def currency_data():
    """ All countries' currency data """
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'currencies.json')
    with open(file_path,'r', encoding='utf-8') as f:
        currency_data = json.loads(f.read())
    return currency_data

def converter(request):
    return render(request, "converter.html", {"currency_data": currency_data})

def converter_results(request):
    # Patikrina, ar užklausa yra POST tipo
    if request.method == "POST":

        # Gauna duomenis iš HTML formos
        currency_from = request.POST.get("currency_from")
        currency_to = request.POST.get("currency_to")
        data = currency_data()
        for row in data:
            if currency_from == row['cc']:
                country_from = row['country']
            if currency_to == row['cc']:
                country_to = row['country']

        # Tikriname, ar įvestis yra validus skaičius
        amount_str = request.POST.get('amount').replace(',', '.')

        # Patikrinimas, ar įvestas tekstas yra tinkamas skaičius
        if not re.match(r'^-?\d+(?:\.\d+)?$', amount_str):
            return render(request, "converter.html",
                          {"currency_data": currency_data(), "error_message": "Only numbers are allowed"})
        try:
            amount = float(amount_str)
        except ValueError:
            return render(request, "converter.html",
                          {"currency_data": currency_data(), "error_message": "Invalid input"})
        # Gauna valiutos keitimo kursus
        url = f"https://open.er-api.com/v6/latest/{currency_from}"
        d = requests.get(url).json()
        # Atlieka konversiją
        if d["result"] == "success":
            # Gauti konversijos kursą norimai valiutai
            ex_target = d["rates"][currency_to]

            # Padauginti iš sumos, kad gauti konvertuotą rezultatą
            result = ex_target * amount

            # Nustato rezultatui 2 skaitmenis po kablelio
            result = "{:.2f}".format(result)

            context = {
                "result": result,
                "amount":amount,
                "country_from":country_from,
                "country_to":country_to,
                "currency_from":currency_from,
                "currency_to": currency_to,
                "currency_data": currency_data(),
            }
            # Pateikia "converter_results.html" šabloną su rezultatu ir kitais duomenimis
            return render(request, "converter_results.html", context)

    # Jei užklausa nėra POST tipo, pateikti "converter.html" šabloną
    return render(request, "converter.html", {"currency_data": currency_data})
