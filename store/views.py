from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, Q

from .models import Author, Book, Customer, Order, OrderItem
from .forms import AuthorForm, BookForm, CustomerForm, OrderForm, OrderItemForm

# Author Views
class AuthorListView(ListView):
    model = Author
    template_name = 'store/author_list.html'
    context_object_name = 'authors'
    paginate_by = 10

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'store/author_detail.html'
    context_object_name = 'author'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.book_set.all()
        return context

class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'store/author_form.html'
    success_url = reverse_lazy('author_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Author created successfully!')
        return super().form_valid(form)

class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'store/author_form.html'
    
    def get_success_url(self):
        return reverse_lazy('author_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Author updated successfully!')
        return super().form_valid(form)

class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    template_name = 'store/author_confirm_delete.html'
    success_url = reverse_lazy('author_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Author deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Book Views
class BookListView(ListView):
    model = Book
    template_name = 'store/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(author__name__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset

class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'store/book_form.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'store/book_form.html'
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'store/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Customer Views
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'store/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'store/customer_detail.html'
    context_object_name = 'customer'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.order_set.all().order_by('-created_at')
        return context

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'store/customer_form.html'
    success_url = reverse_lazy('customer_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer created successfully!')
        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'store/customer_form.html'
    
    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully!')
        return super().form_valid(form)

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'store/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Customer deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Order Views
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    ordering = ['-created_at']

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'store/order_detail.html'
    context_object_name = 'order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context

@login_required
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            messages.success(request, 'Order created successfully!')
            return redirect('order_add_items', pk=order.pk)
    else:
        order_form = OrderForm()
    
    return render(request, 'store/order_form.html', {
        'form': order_form
    })

@login_required
def add_order_items(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
            
            # Update order total
            order.total_amount = order.items.aggregate(
                total=Sum(F('price') * F('quantity'))
            )['total'] or 0
            order.save()
            
            messages.success(request, 'Item added to order!')
            return redirect('order_add_items', pk=order.pk)
    else:
        form = OrderItemForm(initial={'order': order})
    
    # Get existing items
    items = order.items.all()
    
    return render(request, 'store/order_add_items.html', {
        'form': form,
        'order': order,
        'items': items
    })

@login_required
def remove_order_item(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    order = item.order
    item.delete()
    
    # Update order total
    order.total_amount = order.items.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0
    order.save()
    
    messages.success(request, 'Item removed from order!')
    return redirect('order_add_items', pk=order.pk)

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'store/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Order deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Home page view
def home(request):
    recent_books = Book.objects.all().order_by('-created_at')[:6]
    return render(request, 'store/home.html', {
        'recent_books': recent_books
    })

# Search functionality
def search(request):
    query = request.GET.get('q', '')
    books = []
    
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__name__icontains=query) |
            Q(description__icontains=query)
        )
    
    return render(request, 'store/search_results.html', {
        'books': books,
        'query': query
    })