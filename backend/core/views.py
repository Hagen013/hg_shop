from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404

from digg_paginator import DiggPaginator
from rest_framework import mixins, viewsets

from .models import ProductPage, CategoryPage, ProductPhoto
from .serializers import ProductPageSerializer


class IndexPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexPageView, self).get_context_data(*args, **kwargs)
        context['showcase_items'] = ProductPage.public.filter(
            is_bestseller=True)
        context['new_items'] = ProductPage.public.filter(is_new_product=True)
        return context


class CategoryPageView(ListView):
    """
    Класс-контроллер для вывода всех товаров определенной категории
    """
    template_name = "pages/category_page.html"
    context_object_name = 'items_list'
    paginator_class = DiggPaginator
    paginate_by = 40

    def __init__(self, *args, **kwargs):
        super(CategoryPageView, self).__init__(*args, **kwargs)
        self.category = None

    def get(self, request, *args, **kwargs):
        self.category = self.get_category()
        self.sorted = False

        sorting_option    = request.GET.get('o')
        sorting_direction = request.GET.get('dir')

        # На случай прихода GET-запроса с отсутствующим ?dir
        if sorting_direction not in ['ascending', 'descending']:
            sorting_direction = 'descending'
        self.sorting_direction = sorting_direction

        # Чтобы не допустить передачи в качестве аргумента order_by()
        # недопустимых параметров
        if sorting_option in ['scoring', 'price']:
            self.sorting_option = sorting_option
            self.sorted = True
            if sorting_option == 'scoring':
                if self.sorting_direction == 'descending':
                    self.sort_by = ['-scoring', 'price']
                else:
                    self.sort_by = ['scoring', 'price']
            else:
                self.sorting_option = 'price'
                if self.sorting_direction == 'descending':
                    sorting_option = '-' + sorting_option
                self.sort_by = [sorting_option, ]
        else:
            self.sort_by = ['-scoring', 'price']
            self.sorting_option = 'scoring'

        return (super(CategoryPageView, self).get(request, *args, **kwargs))

    def get_category(self):
        url = self.kwargs.get('category_url')
        if url:
            category = get_object_or_404(CategoryPage.objects, url=url)
            return category
        else:
            return None

    def get_queryset(self):
        if self.category:
            qs = ProductPage.objects.filter(
                category__in=self.category.get_descendants(include_self=True)).order_by(*self.sort_by)
        else:
            qs = ProductPage.public.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(CategoryPageView, self).get_context_data(**kwargs)
        context['category'] = self.category

        context['sorting_option'] = self.sorting_option
        context['sorting_direction'] = self.sorting_direction
        context['sorted'] = self.sorted

        if self.category.is_leaf_node():
            if self.category.is_root_node():
                context['category_nodes'] = []
            else:
                context['category_nodes'] = self.category.get_siblings()
            context['is_leaf'] = True
        else:
            context['category_nodes'] = self.category.get_children()
            context['is_leaf'] = False

        if self.category:
            breadcrumbs = self.category.get_ancestors()
            context['breadcrumbs'] = breadcrumbs
        return context

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        return (super(CategoryPageView, self).get_paginator(
            queryset,
            per_page,
            orphans=0,
            allow_empty_first_page=True,
            body=5,
            tail=2,
            **kwargs))


class ProductPageView(TemplateView):
    """
    Класс-контроллер для отображения информации о продукте
    """
    template_name = 'pages/product_page.html'

    def get_template_names(self):
        if 'bruschatka' in self.item.category.url:
            return 'pages/led-stone.html'
        return [self.template_name]

    def get_user_status(self, *args, **kwargs):
        user = self.request.user
        return user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(ProductPageView, self).get_context_data(**kwargs)
        slug = kwargs['slug']
        item = get_object_or_404(ProductPage, slug=slug)
        self.item = item
        if item.category is not None:
            breadcrumbs = item.category.get_ancestors(include_self=True)
        else:
            breadcrumbs = []
        context['item'] = item
        context['breadcrumbs'] = breadcrumbs
        context['attributes'] = item.sorted_attributes

        photos = ProductPhoto.objects.filter(product=item)
        gallery_flag = False
        if len(photos) > 0:
            gallery_flag = True
            context['photos'] = photos
        context['gallery_flag'] = gallery_flag

        context['is_staff'] = self.get_user_status()

        return context


class CatalogRootView(ListView):
    template_name = 'pages/catalog_root.html'
    context_object_name = 'categories_qs'

    def get_queryset(self):
        qs = CategoryPage.objects.filter(level=0)
        return qs


class ProductPageViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or created.
    """
    queryset = ProductPage.objects.all()
    serializer_class = ProductPageSerializer
