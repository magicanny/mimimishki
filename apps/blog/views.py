from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import ListView, DetailView

from apps.blog.forms import SearchForm
from apps.blog.models import Post, Category


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3


class PostDetailView(DetailView):
    queryset = Post.published.all()
    context_object_name = 'post'
    template_name = 'blog/post/detail.html'


class PostSearchView(ListView):
    form_class = SearchForm
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 4

    def get_queryset(self):
        if 'query' in self.request.GET:
            form = self.form_class(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('title', 'body', config='russian')
                search_query = SearchQuery(query, config='russian')
                search_rank = SearchRank(search_vector, search_query)
                queryset = Post.published.annotate(
                    search=search_vector,
                    rank=search_rank
                ).filter(search=search_query).order_by('-rank')

                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query')
        return context


class PostCategoryView(ListView):
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    category = None
    paginate_by = 4

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Post.published.filter(category__slug=self.category.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

