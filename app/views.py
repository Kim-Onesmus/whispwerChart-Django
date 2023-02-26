from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .models import Client, UserSong
from .forms import UserSongForm
import whisper
import os

# Create your views here.

def Splash(request):
    return render(request, 'app/splash.html')

def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if Client.objects.filter(username=username).exists():
                messages.error(request, 'Username exist')
                return redirect('register')
            elif Client.objects.filter(email=email).exists():
                messages.error(request, 'Email exist')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                client_details = Client.objects.create(username=username, email=email, password=password1)
                client_details.save()

                messages.info(request, 'Account created')
                return redirect('login')
        else:
            messages.error(request, 'Password not same')
            return redirect('register')
    else:
        return render(request, 'app/register.html')
    return render(request, 'app/register.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password,)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid details')
            return redirect('login')
    else:
        return render(request, 'app/login.html')
    return render(request, 'app/login.html')
def Home(request):
    form = UserSongForm()
    if request.method == 'POST':
        form = UserSongForm(request.POST, request.FILES)
        if form.is_valid():
            model = whisper.load_model("base")
            
            audio = whisper.load_audio("media/media/{form.music}")
            audio = whisper.pad_or_trim(audio)
            messages.info(request, 'Trimming Audio')
            
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            _, probs = model.detect_language(mel)
            messages.info(request, (f"Detected language: {max(probs, key=probs.get)}"))
            
            options = whisper.DecodingOptions(fp16 = False)
            messages.info(request, 'Decoding Audio')
            result = whisper.decode(model, mel, options)
            messages.info(request, 'Printing results')
            print(result.text)
            
            form.save()
            messages.info(request, 'Audio transcribed')
            return redirect('home')
        else:
            return render(request, 'app/home.html', {'output':output})
    context = {'form':form}
    return render(request, 'app/home.html', context)

def Logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    return render(request, 'app/logout.html')