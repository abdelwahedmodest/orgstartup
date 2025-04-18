from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request, 'accounts/profile.html')

def generate_org_chart_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="organizational_chart.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    data = [
        ["CEO", ""],
        ["COO", "CTO"],
        ["Digital Marketing Manager", "Business Developer"],
        ["Media Buyer", "SEO Specialist"],
        ["Account Manager","Project Manager"],
        ["Backend Developers","Frontend Developers"],
        ["E-commerce Specialist", ""],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    table.wrapOn(p, 400, 200)
    table.drawOn(p, 30, 500)

    textobject = p.beginText(50, 750)
    textobject.setTextOrigin(50, 750)
    textobject.setFont("Helvetica-Bold", 16)
    textobject.textLine("Organizational Chart")
    p.drawText(textobject)

    p.save()
    return response
