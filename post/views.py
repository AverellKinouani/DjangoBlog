from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from .models import Post, Category
from .forms import ContactForm, PostCreationForm
from taggit.models import Tag
from django.contrib.auth.decorators import login_required


def posts_list(request):
    all_published_posts = Post.published.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_published_posts, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts}
    return render(request, 'post/list.html', context)


def user_posts_list(request, username=None):
    user_posts = get_object_or_404(Post, username=username)
    context = {'posts': user_posts}
    return render(request, 'post/posts_list.html', context)


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                             status='published',
                             publish_at__year=year,
                             publish_at__month=month,
                             publish_at__day=day)

    context = {'post': post}
    return render(request, 'post/detail.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category_posts = category.post_set.all()
    context = {'posts': category_posts, 'category': category}
    return render(request, 'post/list.html', context)


def contact(request):
    contact_form = ContactForm()
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            sender_email = contact_form.cleaned_data["email"]
            subject = contact_form.cleaned_data["subject"]
            message = contact_form.cleaned_data["message"]
            send_mail(subject, message, sender_email, ['enquiry@exampleco.com'])
            return HttpResponse("Vote message a été envoyé")
        else:
            return HttpResponse("Echec d'envoie du message")

    context = {'contact_form': contact_form}
    return render(request, 'post/contact.html', context)

def search(request):
    q = request.GET.get('q', None)

    if q is None or q is "":
        searched_posts = Post.published.all()
    elif q:
        searched_posts = Post.published.filter(
            Q(content__icontains=q) | Q(title__icontains=q)
        ).distinct()
    

    page = request.GET.get('page', 1)
    paginator = Paginator(searched_posts, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts}
    return render(request, 'post/list.html', context)


def tag(request, tag):
    tag = get_object_or_404(Tag, name=tag)
    print(tag)
    posts = Post.published.filter(tags__exact=tag)
    return render(request, 'post/list.html', {'posts': posts})


def success(request):
    return HttpResponse('Success! Thank you for your message.')


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        post_creation_form = PostCreationForm(request.POST, request.FILES)
        if post_creation_form.is_valid():
            title = post_creation_form.cleaned_data['title']
            summary = post_creation_form.cleaned_data['summary']
            content = post_creation_form.cleaned_data['content']
            category = post_creation_form.cleaned_data['category']
            picture = post_creation_form.cleaned_data['picture']
            tags = post_creation_form.cleaned_data['tags']
            author = request.user

            post = Post(title=title, summary=summary, content=content, category=category, picture=picture,
                        author=author)
            post.save()
            message.success("Votre article a été sauvegardé.")
    else:
        post_creation_form = PostCreationForm()
    return render(request, 'account/post_creation.html', {'form': post_creation_form})


@login_required(login_url='login')
def update_post(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                             status='published',
                             publish_at__year=year,
                             publish_at__month=month,
                             publish_at__day=day)

    if request.user != post.author:
        raise PermissionDenied()

    if request.method == 'POST':
        post_creation_form = PostCreationForm(
            request.POST, request.FILES, instance=post)
        if post_creation_form.is_valid():
            title = post_creation_form.cleaned_data['title']
            summary = post_creation_form.cleaned_data['summary']
            content = post_creation_form.cleaned_data['content']
            category = post_creation_form.cleaned_data['category']
            picture = post_creation_form.cleaned_data['picture']
            tags = post_creation_form.cleaned_data['tags']
            author = request.user

            post = Post(title=title, summary=summary, content=content, category=category, picture=picture,
                        author=author)
            post.save()
            message.success("Votre article a été mis à jour.")
    else:
        post_creation_form = PostCreationForm(instance=post)

    return render(request, 'account/update-post.html', {'post_creation_form': post_creation_form})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('/success')
