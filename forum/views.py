from django.shortcuts import render
from django.views.decorators.gzip import gzip_page
from django.shortcuts import render_to_response,render
from django.template import RequestContext,Context,Template
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
from django.utils.translation import ugettext as _
import markdown

from .utils import group_required
from .models import Thread,Category,Post,Document,UserProfile
from .forms import DocumentForm,AddThreadForm,AddCategoryForm,EditThreadForm,QuoteThreadForm,AddPostForm,SearchForm
from django.contrib.auth.decorators import login_required
import logging


def list(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

def home(request):
    time=datetime.datetime.now()
    threads=[]
    threads=Thread.objects.all().order_by("-id")[0:10]
    categories=Category.objects.all()
    variables={'threads':threads,'categories':categories,'time':time}
    return render_to_response('homepage.html',variables,context_instance=RequestContext(request))

def search(request):
    #query=request.POST.get('q','')
    query=request.GET.get('q','')
    results=[]
    if query:
        results=Thread.objects.filter(topic__icontains=query)
    variables={'query':query,'results':results}
    return render_to_response('search.html',
                              variables,context_instance=RequestContext(request))
    
    

def get_category(request,slug):
    try:
        category=Category.objects.get(slug=slug)
    except:
        raise Http404('Does not exist')
    threads=Thread.objects.filter(category=category)
    variables={'category':category,'threads':threads}
    return render_to_response('get_category.html',variables,context_instance=RequestContext(request)) 

@login_required
def new_thread(request,pk):
    category=Category.objects.get(pk=pk)
    if request.method=='POST':
        form=AddThreadForm(request.POST,request.FILES)
        if form.is_valid():
             thread = Thread(
                             topic=request.POST['topic'],
                             image=request.FILES.get('image'),
                             category=category,
                             user=request.user,
                             main_post=request.POST['main_post'],
                             
                             )
             thread.save()
             home(request)
             return HttpResponseRedirect(reverse('get_thread',args=[thread.slug]))
        else:
             form=AddThreadForm(request.POST,request.FILES)
             #new_category(request)
    else:
        form=AddThreadForm()
    variables={'form':form,'category':category}
    return render_to_response('new_thread.html',variables,context_instance=RequestContext(request))


@login_required
def delete_thread(request,slug):
    thread=Thread.objects.get(pk=slug)
    category=thread.category
    if thread.user==request.user:
        thread.delete()
        messages.add_message(request,messages.SUCCESS,_('Deleted'))
    return HttpResponseRedirect(reverse('get_category',args=[category.slug]))





def get_thread(request,slug):
    try:
        thread=Thread.objects.get(slug=slug)
    except:
        raise Http404('Does not exist')
    if thread:
        posts=Post.objects.filter(thread=thread)
        new_post_form=AddPostForm()
        variables={'thread':thread,'new_post_form':new_post_form,'posts':posts}
        return render_to_response('get_thread.html',variables,context_instance=RequestContext(request))
    else:
        raise Http404('Does not exist')



@login_required
def edit_thread(request,slug):
    try:
        thread=Thread.objects.get(pk=slug)
    except ValueError:
        raise Http404('Does not exist')
    if request.user!=thread.user:
        raise Http404('not authorized')
    else:
        if request.POST:
            form=AddThreadForm(request.POST,request.FILES,instance=thread)
            if form.is_valid():
                form.save()
                messages.add_message(request,messages.SUCCESS,_('Topic saved.'))
                return HttpResponseRedirect(reverse('get_thread',
                                                    args=[thread.slug]))

            else:
                pass
              
        else:
            form=AddThreadForm(instance=thread)
        variables={'form':form}
        return render_to_response('edit_thread.html',
                                  variables,
                                  context_instance=RequestContext(request))

@login_required
def quote_thread(request,slug):
    try:
        post=Post.objects.get(pk=slug)
    except ValueError:
        raise Http404('Does not exist')
   
    if request.POST:
        form=QuoteThreadForm(request.POST,instance=post)
        if form.is_valid():
            quote=request.POST.get('quote')
            quote=post.post+quote
            new_Post=Post(thread=post.thread,post=quote,user=request.user,post_type="quote")
            new_Post.save()
            messages.add_message(request,messages.SUCCESS,_('Quote saved.'))
                
        else:
            pass
              
    else:
        form=QuoteThreadForm(instance=post)
    t=Template("My name is {{ request.user.username }}")
    d={}
    t.render(Context(d))
    quoted_text= render(request,
                        'quoted_text.txt',{},
                        content_type="text/plain")
    quoted_text='hi'
    variables={'form':form,'quoted_text':quoted_text,'post':post}
    return render_to_response('quote_thread.html',variables,context_instance=RequestContext(request))


'''

@group_required('site-admin','moderators')
'''

@login_required
def new_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = AddCategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)

            return home(request)
        else:
            pass
    else:
        form = AddCategoryForm()

    return render_to_response('add_category.html', {'form': form}, context)


def user_page(request,username):
    if User.objects.filter(username=username).exists():
        user=User.objects.get(username=username)
        threads=Thread.objects.filter(user=user)
        pic=UserProfile.objects.get(user=user).pic
    else:
        raise Http404('User does not exist')
    variables={'user':user,'threads':threads,'pic':pic}
    return render_to_response('user_page.html',variables,context_instance=RequestContext(request))

@login_required
def edit_user_page(request,username):
    if User.objects.filter(username=username).exists() and username==request.user.username:
        user=User.objects.get(username=username)
    else:
        raise Http404('You are not authorized to view this page')
    
        
    if request.method=='POST':
        first_name=request.POST.get('first_name','')
        last_name=request.POST.get('last_name','')
        email=request.POST.get('email','')
        pic=request.FILES['dp']
        if pic:
            UserProfile(user=user,pic=pic).save()
        if email and user.email!=email and email != '':
            print("got here")
            user.email=email
            user.save()
            messages.add_message(request,messages.SUCCESS,_('Changes saved'))
        if last_name and user.last_name!=last_name and last_name!='':
            user.last_name=last_name
            user.save()
            messages.add_message(request,messages.SUCCESS,_('Changes saved'))
        if first_name and user.first_name!=last_name and first_name!='':
            user.first_name=first_name
            user.save()
            messages.add_message(request,messages.SUCCESS,_('Changes saved'))
        variables={'last_name':last_name,'email':email}
        return render_to_response('edit_user_page.html',variables,context_instance=RequestContext(request))

    elif request.method=='GET' :
        variables={}
        return render_to_response('edit_user_page.html',variables,context_instance=RequestContext(request))


@login_required
def add_post(request,pk):
    try:
        thread=Thread.objects.get(pk=pk)
    except thread.DoesNotExist:
        raise Http404('Does not exist')
    if request.method=='POST':
        form=AddPostForm(request.POST)
        if form.is_valid():
             post = form.save(commit = False)
             post.thread=thread
             post.user=request.user
             post.save()
             form.save_m2m()
             return HttpResponseRedirect(reverse('get_thread',args=[thread.slug]))
        else:
             form=AddThreadForm(request.POST)
             
    else:
        form=AddThreadForm()
    variables={'form':form,'thread':thread}
    return render_to_response('new_post.html',variables,context_instance=RequestContext(request))
