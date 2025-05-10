from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib import messages

# Blog List View
def blog_list(request):
    posts = BlogPost.objects.filter(status='approved').order_by('-published_at')
    return render(request, 'blog_list.html', {'posts': posts})

# Blog Detail View
def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, status='approved')
    return render(request, 'blog_detail.html', {'post': post})

# Submit Blog Post View
@login_required
def submit_blog(request):
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user  
            blog_post.status = 'pending'
            blog_post.save()
            messages.success(request, 'Your blog post has been submitted and is awaiting approval.')
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'submit_blog.html', {'form': form})