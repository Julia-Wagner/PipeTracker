import csv
import qrcode
import io
from decimal import Decimal, DecimalException

from cloudinary import uploader
from django.http import HttpResponseRedirect
from django.views.generic import (CreateView, ListView, DeleteView, UpdateView,
                                  FormView, DetailView)
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django_tables2 import RequestConfig
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin

from basket.models import BasketItem, Basket
from .models import Category, Item
from .forms import CategoryForm, ItemForm, UploadForm
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

        context["breadcrumbs"] = category.get_breadcrumbs()
        context["category"] = category
        return context


class AddCategory(CreateView):
    """
    Add Category view
    """
    template_name = "stock/add_category.html"
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("stock_categories")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(AddCategory, self).form_valid(form)
        # add success message
        messages.success(self.request,
                         "Category created successfully.")
        return response


class DeleteCategory(UserPassesTestMixin, DeleteView):
    """
    Delete a Category
    """
    model = Category
    success_url = reverse_lazy("stock_categories")

    # check if user is superuser
    def test_func(self):
        return self.request.user.is_superuser

    # show error message for normal users
    def handle_no_permission(self):
        messages.error(self.request,
                       "You are not allowed to delete a category.")
        return super().handle_no_permission()

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
    success_url = reverse_lazy("stock_categories")

    # add success message
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Changes saved.")
        return response


class SearchItems(ListView):
    """
    List all stock items from the search query
    """
    template_name = "stock/items.html"
    model = Item
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get items from search query
        query = self.request.GET.get("q")
        if query:
            items = self.model.objects.filter(
                Q(name__icontains=query) |
                Q(size__icontains=query) |
                Q(matchcode__icontains=query)
            )
        else:
            # get all stock items
            items = self.model.objects.all()

        # create and configure stock items table
        table = ItemTable(items)
        RequestConfig(self.request).configure(table)

        context["category"] = query
        context["table"] = table

        return context


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

        # create and configure stock items table
        table = ItemTable(items)
        RequestConfig(self.request).configure(table)

        context["category"] = category.name
        context["breadcrumbs"] = category.get_breadcrumbs()
        context["table"] = table

        return context


class AddItemFromUpload(FormView):
    template_name = "stock/upload_file.html"
    form_class = UploadForm
    success_url = reverse_lazy("stock_categories")

    def form_valid(self, form):
        csv_file = form.cleaned_data["file"]

        try:
            # read the uploaded file
            decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
            reader = csv.DictReader(decoded_file, delimiter=";")

            # remove BOM from field names
            # https://github.com/dbt-labs/dbt-core/issues/1177
            reader.fieldnames = [field.lstrip("\ufeff") for field in
                                 reader.fieldnames]

            # make sure the file has the required fields
            required_fields = ["category", "name", "matchcode", "price",
                               "quantity", "size", "details"]
            for field in required_fields:
                if field not in reader.fieldnames:
                    messages.error(
                        self.request,
                        f"Missing field in file: '{field}'. "
                        f"Please upload a valid CSV using the example file.")
                    return super().form_invalid(form)

            # process each row
            counter = 0
            for row in reader:
                # get the values
                category = get_object_or_404(Category, id=int(row["category"]))
                name = row["name"]
                matchcode = row["matchcode"]
                # convert price and set default for missing value
                raw_price = row["price"]
                if raw_price is None or raw_price == "":
                    price = 0.00
                else:
                    try:
                        # https://stackoverflow.com/questions/4643991/python-converting-string-into-decimal-number
                        price = Decimal(raw_price.replace(",", "."))
                    except (ValueError, DecimalException):
                        # no valid integer
                        messages.error(self.request,
                                       f"Invalid price value: "
                                       f"'{raw_price}' for item '{name}'.")
                # convert quantity and set default for missing value
                raw_quantity = row.get("quantity", "1")
                if raw_quantity is None or raw_quantity == "":
                    quantity = 0
                else:
                    try:
                        quantity = int(raw_quantity)
                    except ValueError:
                        # no valid integer
                        messages.error(self.request,
                                       f"Invalid quantity value: "
                                       f"'{raw_quantity}' for item '{name}'.")
                size = row["size"]
                details = row["details"]

                # check if item already exists
                existing_item = Item.objects.filter(
                    matchcode=matchcode).first()

                if not existing_item:
                    # check that all required fields are given
                    if all(value is not None and value.strip() != "" for value
                           in [name, matchcode]):
                        # create a stock item for the row
                        Item.objects.create(
                            user=self.request.user,
                            category=category,
                            name=name,
                            matchcode=matchcode,
                            price=price,
                            quantity=quantity,
                            size=size,
                            details=details
                        )
                        counter += 1
                    else:
                        messages.error(
                            self.request,
                            "One or more required fields missing or empty.")
                else:
                    messages.error(
                        self.request,
                        f"Item '{existing_item.name}' already exists.")

            messages.success(self.request,
                             f"{counter} items created successfully.")
            return super().form_valid(form)

        except Exception:
            messages.error(self.request,
                           "Please upload a valid CSV file.")
            return super().form_invalid(form)


class AddItem(CreateView):
    """
    Add Item view
    """
    template_name = "stock/add_item.html"
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy("stock_categories")

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


class ItemDetail(DetailView):
    """
    Detail view for a stock item
    """
    template_name = "stock/item_detail.html"
    model = Item
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # create the QR code
        # https://pypi.org/project/qrcode/
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # add the link to the code
        absolute_url = self.request.build_absolute_uri(
            reverse_lazy("stock_item_detail", args=[self.kwargs["pk"]])
        )
        qr.add_data(absolute_url)
        qr.make(fit=True)

        # generate image from the code
        img = qr.make_image(fill_color=(39, 64, 96),
                            back_color=(229, 231, 235))

        # save image
        # https://cloudinary.com/documentation/upload_images
        buffer = io.BytesIO()
        img.save(buffer, kind="PNG")

        response = uploader.upload(buffer.getvalue(), folder="qr_codes")

        context["qr_image"] = response["secure_url"]
        return context


class ItemToBasket(View):
    """
    Add Item to basket view
    """

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # https://stackoverflow.com/questions/150505/how-to-get-get-request-values-in-django
        quantity_param = request.GET.get("quantity", "1")
        # convert to float and then int to ensure correct value
        quantity = int(float(quantity_param))
        item_id = self.kwargs.get("pk")
        item = get_object_or_404(Item, id=item_id)

        # get the redirect url
        category_id = item.category.id
        redirect_url = reverse_lazy("stock_items", kwargs={"pk": category_id})
        previous_url = request.META.get("HTTP_REFERER")

        # check if quantity is available
        if quantity > item.quantity:
            messages.error(request,
                           f"{item}: only {item.quantity} available.")
            return HttpResponseRedirect(redirect_url)

        # get or create users basket
        basket, created = Basket.objects.get_or_create(user=user)

        # check if item is already in basket
        exists = BasketItem.objects.filter(basket=basket, item=item).exists()

        # update item if already in basket
        if exists:
            basket_item = BasketItem.objects.get(basket=basket, item=item)
            basket_item.quantity += quantity
            basket_item.save()
        # create new item
        else:
            BasketItem.objects.create(basket=basket, item=item,
                                      quantity=quantity),

        # reduce stock item quantity
        item.quantity -= quantity
        item.save()

        messages.success(request,
                         f"{item} ({quantity}) added to your basket.")

        return redirect(previous_url or redirect_url)


class StockItemDecrease(View):
    """
    Decrease the quantity of the stock item
    """
    def get(self, request, *args, **kwargs):
        # store last URL
        request.session["previous_url"] = (
            self.request.META.get("HTTP_REFERER", None))

        stock_item_id = self.kwargs.get("pk")
        stock_item = get_object_or_404(Item, id=stock_item_id)

        if stock_item.quantity >= 1:
            # decrease stock item quantity
            stock_item.quantity -= 1
            stock_item.save()

            messages.success(request,
                             f"{stock_item} quantity changed.")
        else:
            messages.error(request,
                           "Quantity can not be less than 0.")

        # get the success url
        category_id = stock_item.category.id
        success_url = reverse_lazy("stock_items", kwargs={"pk": category_id})
        previous_url = request.META.get("HTTP_REFERER")

        return redirect(previous_url or success_url)


class StockItemIncrease(View):
    """
    Increase the quantity of the stock item
    """
    def get(self, request, *args, **kwargs):
        stock_item_id = self.kwargs.get("pk")
        stock_item = get_object_or_404(Item, id=stock_item_id)

        stock_item.quantity += 1
        stock_item.save()

        messages.success(request,
                         f"{stock_item} quantity changed.")

        # get the success url
        category_id = stock_item.category.id
        success_url = reverse_lazy("stock_items", kwargs={"pk": category_id})
        previous_url = request.META.get("HTTP_REFERER")

        return redirect(previous_url or success_url)
