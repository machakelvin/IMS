from django.shortcuts import render , redirect 
from django.views.generic import TemplateView 
from .models import InventoryItem, Category
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login 
from .forms import UserRegisterForm, InventoryItemForm
from .views import InventoryItem
from django.views import View
from django.http import HttpResponseRedirect
from django.db.models import F
from django.contrib import messages
from IMS.settings import LOW_QUANTITY
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
class Index(TemplateView):
    template_name = 'inventory/index.html'
    

class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')
        
        low_inventory = InventoryItem.objects.filter(
            user=self.request.user.id, 
            quantity__lte= LOW_QUANTITY
             )
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items are running low on inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item is running low on inventory')    
        
        low_inventory_ids = InventoryItem.objects.filter(
            user=self.request.user.id, 
            quantity__lte= LOW_QUANTITY
             ).values_list('id', flat=True)
        
        return render(request, 'inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})
     


class SignupView(View):
    def get(self, request,):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('index')
        return render(request, 'inventory/signup.html', {'form': form})
    


class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Get the cleaned data from the form
        name = form.cleaned_data['name']
        category = form.cleaned_data['category']
        quantity = form.cleaned_data['quantity']
        
        # Check if an item with the same name and category exists for this user
        existing_item = InventoryItem.objects.filter(name=name, category=category, user=self.request.user).first()

        if existing_item:
            # If it exists, update the quantity instead of creating a new one
            existing_item.quantity = F('quantity') + quantity
            existing_item.save()
            # Redirect to the dashboard after updating
            return HttpResponseRedirect(self.success_url)
        
        # If no existing item, create a new item and assign the current user
        form.instance.user = self.request.user
        return super().form_valid(form)

    
class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    temmplate_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')
    
    
class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'