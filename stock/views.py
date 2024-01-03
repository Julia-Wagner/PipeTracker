from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.views import View
from django.shortcuts import get_object_or_404
from django_tables2 import RequestConfig
from django.urls import reverse_lazy
from django.contrib import messages

from basket.models import BasketItem, Basket
from .models import Category, Item
from .forms import CategoryForm, ItemForm
from .tables import ItemTable


class Categories(ListView):
    """
    List all categories
    """
    template_name = "stock/categories.html"
    model = Category
    context_object_name = "categories"

    # filter for parent categories only
    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)


class CategoriesChildren(ListView):
    """
    List all child categories
    """
    template_name = "stock/categories_children.html"
    context_object_name = 'children'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs["pk"])
        return category.children.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the current category
        category = get_object_or_404(Category, id=self.kwargs["pk"])
        parents = category.get_parents()
        breadcrumbs = []
        # add all parents to breadcrumbs
        for parent in parents:
            breadcrumbs.append({"name": parent.name, "id": parent.id})
        # add current category to breadcrumbs
        breadcrumbs.append({"name": category.name, "id": category.id})
        context["breadcrumbs"] = breadcrumbs
        context["category"] = category
        return context


class AddCategory(CreateView):
    """
    Add Category view
    """
    template_name = "stock/add_category.html"
    model = Category
    form_class = CategoryForm
    success_url = "/stock/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(AddCategory, self).form_valid(form)
        # add success message
        messages.success(self.request,
                         "Category created successfully.")
        return response


class DeleteCategory(DeleteView):
    """
    Delete a Category
    """
    model = Category
    success_url = "/stock/"

    # add success message
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Category deleted.")
        return response


class EditCategory(UpdateView):
    """
    Edit a Category
    """
    template_name = "stock/edit_category.html"
    model = Category
    form_class = CategoryForm
    success_url = "/stock/"

    # add success message
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Changes saved.")
        return response


class Items(ListView):
    """
    List all stock items
    """
    template_name = "stock/items.html"
    model = Item
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get the current category
        category = get_object_or_404(Category, id=self.kwargs["pk"])
        items = category.stock_items.all()
        fields = ("name", "size", "matchcode", "details", "price", "quantity")

        # create and configure stock items table
        table = ItemTable(items)
        RequestConfig(self.request).configure(table)

        # create stock items dictionary
        items_dic = []
        for item in items:
            item_dic = {}
            for field in fields:
                item_dic[field] = getattr(item, field)
            items_dic.append(item_dic)

        context["category"] = category
        context["table"] = table
        context["items_dic"] = items_dic

        return context


class AddItem(CreateView):
    """
    Add Item view
    """
    template_name = "stock/add_item.html"
    model = Item
    form_class = ItemForm
    success_url = "/stock/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(AddItem, self).form_valid(form)
        # add success message
        messages.success(self.request,
                         "Stock Item created successfully.")
        return response


class EditItem(UpdateView):
    """
    Edit a Stock Item
    """
    template_name = "stock/edit_item.html"
    model = Item
    form_class = ItemForm

    def get_success_url(self):
        # get the current category
        category_id = self.object.category.id

        success_url = reverse_lazy("stock_items", kwargs={"pk": category_id})
        return success_url

    # add success message
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Changes saved.")
        return response


class DeleteItem(DeleteView):
    """
    Delete a Stock Item
    """
    model = Item

    def get_success_url(self):
        # get the current category
        category_id = self.object.category.id

        success_url = reverse_lazy("stock_items", kwargs={"pk": category_id})
        return success_url

    # add success message
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Stock Item deleted.")
        return response


class ItemToBasket(View):
    """
    Add Item to basket view
    """

    def get(self, request, *args, **kwargs):
        user = self.request.user
        item_id = self.kwargs.get("pk")
        item = get_object_or_404(Item, id=item_id)

        # get or create users basket
        basket, created = Basket.objects.get_or_create(user=user)

        # check if item is already in basket
        exists = BasketItem.objects.filter(basket=basket, item=item).exists()

        # update item if already in basket
        if exists:
            basket_item = BasketItem.objects.get(basket=basket, item=item)
            basket_item.quantity += 1
            basket_item.save()
        # create new item
        else:
            BasketItem.objects.create(basket=basket, item=item, quantity=1)

        messages.success(request, f"{item} added to your basket.")

        # get the success url
        category_id = item.category.id
        success_url = reverse_lazy("stock_items", kwargs={"pk": category_id})
        return HttpResponseRedirect(success_url)
