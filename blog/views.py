from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from blog import forms, models


@login_required
def home(request):
    blogs = models.Blog.objects.all()
    return render(request, 'blog/home.html', context={'blogs': blogs})

@login_required
def blog_upload(request):
    blog_form = forms.BlogForm()
    if request.method == 'POST':
        blog_form = forms.BlogForm(request.POST)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('home')
    context = {
        'blog_form': blog_form,
}
    return render(request, 'blog/create_blog_post.html', context=context)


@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})