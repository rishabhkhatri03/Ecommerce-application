from math import ceil
from django.shortcuts import render
from ecommerce_app.models import Contact, Product
from django.contrib import messages

def index(request):
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n/4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, "index.html", params)

def contact(request):
    if request.method == "POST":
        # Get the form data from the POST request
        name = request.POST.get("fname")
        email = request.POST.get("contactEmail")
        phone = request.POST.get("contactPhone")
        message = request.POST.get("comment")
        
        # Create a new Contact object and save it to the database
        myquery = Contact(name=name, email=email, phone_number=phone, message=message)
        myquery.save()  # Save the contact entry
        messages.success(request, "We will get back to you soon!!!")
        return render(request, "contact.html")

    # If not POST, render the empty contact form
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")
