from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


from .models import Like, Video, Comment, Category
from .forms import CommentForm, VideoForm

# Create your views here.

class Index(ListView):
    model = Video
    template_name = 'video_stream/index.html'
    order_by = '-date_posted'


# class UploadVideo(LoginRequiredMixin, CreateView):
#     model = Video
#     form_class = VideoForm
#     # fields = ['title', 'description', 'video_file', 'thumbnail', 'category']
#     template_name = 'video_stream/upload.html'

#     def form_valid(self, form):
#         form.instance.uploader = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('video_detail', kwargs={'pk': self.object.pk})

class UploadVideo(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'video_stream/upload.html'

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        # Get the category instance from the form data
        category_id = self.request.POST.get('categories')
        category = get_object_or_404(Category, pk=category_id)
        form.instance.category = category  # Set the category for the video
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video_detail', kwargs={'pk': self.object.pk})


'''class VideoCategory(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'video_stream/category.html'

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('upload')'''
        
class VideoCategory(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'video_stream/category.html'

    def form_valid(self, form):
        # Check if the category already exists
        category_name = form.cleaned_data['name']
        existing_category = Category.objects.filter(name=category_name).first()
        
        if existing_category:
            # If the category already exists, redirect to the upload page or handle it as desired
            return HttpResponseRedirect(reverse('upload'))
        else:
            # If the category does not exist, create it
            form.instance.uploader = self.request.user
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('upload')



# class VideoDetail(View):
#     def get(self, request, pk, *args, **kwargs):
#         video = get_object_or_404(Video, pk=pk)

#         # Increment view count
#         video.view_count += 1
#         video.save()

#         form = CommentForm()
#         comments = Comment.objects.filter(video=video).order_by('-created_on')
#         categories = Video.objects.filter(category=video.category)[:15]

#         # Ensure default values are set to 0 for likes and unlikes
#         likes = Like.objects.filter(video=video, is_like=True).count() if Like.objects.filter(video=video, is_like=True).exists() else 0
#         unlikes = Like.objects.filter(video=video, is_like=False).count() if Like.objects.filter(video=video, is_like=False).exists() else 0

#         context = {
#             'object': video,
#             'comments': comments,
#             'categories': categories,
#             'form': form,
#             'likes': likes,
#             'unlikes': unlikes,
#         }
#         return render(request, 'video_stream/detail_video.html', context)

class VideoDetail(View):
    def get(self, request, pk, *args, **kwargs):
        video = get_object_or_404(Video, pk=pk)

        # Increment view count
        video.view_count += 1
        video.save()

        form = CommentForm()
        comments = Comment.objects.filter(video=video).order_by('-created_on')

        # Get the category of the video
        category = video.category

        # Ensure default values are set to 0 for likes and unlikes
        likes = Like.objects.filter(video=video, is_like=True).count() if Like.objects.filter(video=video, is_like=True).exists() else 0
        unlikes = Like.objects.filter(video=video, is_like=False).count() if Like.objects.filter(video=video, is_like=False).exists() else 0

        context = {
            'object': video,
            'comments': comments,
            'category': category,  # Add category to the context
            'form': form,
            'likes': likes,
            'unlikes': unlikes,
        }
        return render(request, 'video_stream/detail_video.html', context)


    def post(self, request, pk, *args, **kwargs):
        video = get_object_or_404(Video, pk=pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                user=self.request.user,
                comment=form.cleaned_data['comment'],
                video=video
            )
            comment.save()

        # Handle like/unlike
        is_like = 'like' in request.POST
        like, created = Like.objects.update_or_create(video=video, user=request.user, defaults={'is_like': is_like})
        if not created:
            like.delete()
        
        comments = Comment.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:15]

        # Ensure default values are set to 0 for likes and unlikes
        likes = Like.objects.filter(video=video, is_like=True).count() if Like.objects.filter(video=video, is_like=True).exists() else 0
        unlikes = Like.objects.filter(video=video, is_like=False).count() if Like.objects.filter(video=video, is_like=False).exists() else 0

        context = {
            'object': video,
            'comments': comments,
            'categories': categories,
            'form': form,
            'likes': likes,
            'unlikes': unlikes,
        }
        return render(request, 'video_stream/detail_video.html', context)


class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description']
    template_name = 'video_stream/upload.html'

    def get_success_url(self):
        return reverse('video_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class RemoveVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'video_stream/remove_video.html'

    def get_success_url(self):
        return reverse('index')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class VideoList(View):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        videos = Video.objects.filter(category=pk).order_by('-date_posted')
        context = {
            'category': category,
            'videos': videos
        }

        return render(request, 'video_stream/list.html', context)


# class SearchVideo(View):
#     def get(self, request, *args, **kwargs):
#         query = self.request.GET.get("q")

#         query_list = Video.objects.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(uploader__username__icontains=query)
#         )

#         context = {
#             'query_list': query_list,
#         }

#         return render(request, 'video_stream/search.html', context)


class SearchVideo(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        category_query = self.request.GET.get("category")

        query_list = Video.objects.all()

        if query:
            query_list = query_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(uploader__username__icontains=query)
            )

        if category_query:
            # Filter videos by category name if category query is not None
            query_list = query_list.filter(category__name__contains=category_query)

        context = {
            'query_list': query_list,
        }

        return render(request, 'video_stream/search.html', context)