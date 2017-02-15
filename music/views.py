from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django import forms

from .models import Album,Songs
from rest_framework import generics
from .serializers import AlbumSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from .forms import AlbumForm,UserForm,LoginForm,SongsForm
from .permissions import IsOwnerOrReadOnly
from django.views import generic
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
#login,authentication,redirect,etc
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
#for creating,updating and deleting objects form
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from django.http import JsonResponse,Http404
#login required decorator
from django.contrib.auth.decorators import login_required
#Q lookups
from django.db.models import Q
#class based view(Generic View)



class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_album'
    def get_queryset(self):
        queryset=Album.objects.all()
        query=self.request.GET.get("q")
        if query:
            queryset=queryset.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query) |
                Q(genre__icontains=query) |
                Q(owner__first_name__icontains=query) |
                Q(owner__last_name__icontains=query)
                ).distinct()
        return queryset

class MyAlbumList(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_album'
    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)

class MySongsList(generic.ListView):
    template_name='music/mysongs.html'
    context_object_name='all_songs'

    def get_queryset(self):
        album_qs=Album.objects.filter(owner=self.request.user)
        return Songs.objects.filter(album__in=album_qs) 


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

#creating a form to add albums

class AlbumCreate(CreateView):
    model = Album

    fields = ['artist','album_title','genre','album_logo']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AlbumCreate, self).form_valid(form)

class AlbumUpdate(UpdateView):

    model = Album
    fields = ['artist','album_title','genre','album_logo']

    def dispatch(self,request,*args,**kwargs):
        obj=self.get_object()
        if obj.owner!=self.request.user:
            return redirect(obj)
        return super(AlbumUpdate,self).dispatch(request,*args,**kwargs)    

class AlbumDelete(DeleteView):

    model = Album
    success_url = reverse_lazy('music:index')

    #override get_object method to validate user
    def get_object(self,queryset=None):
        obj=super(AlbumDelete,self).get_object()
        if obj.owner!=self.request.user:
            raise Http404
        return obj    

#User_Registration Class

class UserFormView(View):

    form_class=UserForm
    template_name='music/registration.html'

    #handle get request(Display blank form)
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})


    #handle post request(Register User)
    def post(self,request):

        form=self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commit=False)

            #cleaned(normalised) data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            password1=form.cleaned_data['password1']
            if password!=password1:
                raise forms.ValidationError("Wrong passwords")

            else:
                user.set_password(password)
                user.save()

            #returns User if credentials are correct

                user=authenticate(username=username,password=password)

                if user is not None:
                    if user.is_active:   #account not banned or diabled

                        login(request,user)
                        return  redirect('music:index')


        return render(request,self.template_name,{'form':form})


#Login

class LoginFormView(View):

    form_class=LoginForm
    template_name='music/login.html'

    def get(self,request):

        form=self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
                n=request.GET.get('next')
                form=self.form_class(request.POST)
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)


                if user is not None:
                 if user.is_active:

                    login(request,user)
                    if n:
                        return redirect(n)
                    return redirect('music:index')


                return render(request,self.template_name,{'form':form,'error':"Incorrect Credentials.Try Again"})

#add songs

class SongsView(View):

    form_class=SongsForm
    template_name='music/add_songs.html'

    def get(self,request,album_id):
        form=self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request,album_id):


        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            song=form.save(commit=False)
            al=Album.objects.get(pk=album_id)
            song.album=al
            song.music_file=request.FILES['music_file']
            song.save()
            return redirect('music:detail',album_id)
        else:
            return redirect('music:add_songs',album_id)


#delete song
def songDelete(request,album_id,song_id):

    song=Songs.objects.filter(pk=song_id).first()
    if song.album.owner==request.user:
        song.delete()
        return redirect('music:detail',album_id)
    raise Http404    

#play song
def playSong(request,album_id,song_id):

    song=Songs.objects.get(pk=song_id)
    return render(request,'music/music_player.html',{'song':song})

#logout
def logoutUser(request):

    if request.user.is_authenticated():
        logout(request)
        return render(request,'music/logout.html')
    else:
        return render(request,'music/logout.html',{'error':"User is not Logged In.Login to Logout"})






#function based view

"""
#music_home

def index(request):
    all_album = Album.objects.all()

    context = {
        'all_album': all_album
    }
    return render(request,'music/index.html',context)


#detail

def detail(request,album_id):

   album = get_object_or_404(Album, pk=album_id)
   return render(request,'music/detail.html',{'album': album})

"""


##############################################################################################

#api

def home(request):

    title="Welcome!!! Please Log in to Add Albums"

    if request.user.is_authenticated:
        title="Welcome  back "+str(request.user)
    form = AlbumForm(request.POST or None)
    context={

        'title':title,
        'form':form,
    }



    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        context={
            'title':'Thank You',
        }
    return render(request,'home.html',context)




class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
     queryset = User.objects.all()
     serializer_class = UserSerializer



#favorite
"""
def favorite(request,album_id):

   album = get_object_or_404(Album, pk=album_id)

   try:
       selected=album.songs_set.get(pk=request.POST['song'])

   except (KeyError,Songs.DoesNotExist):
       return render(request,'music/detail.html',{'album': album,

                                                  'error_message':"Not a valid song",

                                                  })
   else:

       if selected.is_fav:
           selected.is_fav= False
       else:selected.is_fav=True
       selected.save()
       return render(request,'music/detail.html',{'album': album})

"""


