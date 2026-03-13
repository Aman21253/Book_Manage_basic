from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book, Student


def is_valid_isbn(isbn):
    isbn = isbn.replace("-", "").replace(" ", "")
    return isbn.isdigit() and len(isbn) in [10, 13]


def login_view(request):
    if request.user.is_authenticated:
        return redirect('book_details')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj = None

        if user_obj is not None:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('book_details')

        messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')


@login_required(login_url='login')
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        author = request.POST.get("author", "").strip()
        isbn = request.POST.get("isbn", "").strip()
        price = request.POST.get("price", "").strip()
        # pages = request.POST.get("pages", "").strip()
        quantity = request.POST.get("quantity", "").strip()
        description = request.POST.get("description", "").strip()

        if not title or not author or not isbn or not price or not quantity or not description:
            messages.error(request, "All fields are required.")
            return render(request, "add_book.html")

        if not is_valid_isbn(isbn):
            messages.error(request, "Invalid ISBN. ISBN must be 10 or 13 digits.")
            return render(request, "add_book.html")

        if Book.objects.filter(isbn=isbn).exists():
            messages.error(request, "A book with this ISBN already exists.")
            return render(request, "add_book.html")

        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Price must be a valid number.")
            return render(request, "add_book.html")

        try:
            quantity = int(quantity)
        except ValueError:
            messages.error(request, "Quantity must be a valid integer.")
            return render(request, "add_book.html")

        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            price=price,
            # pages=pages,
            quantity=quantity,
            description=description
        )

        messages.success(request, "Book added successfully.")
        return redirect("book_details")

    return render(request, "add_book.html")


@login_required(login_url='login')
def book_details(request):
    search_query = request.GET.get("search", "").strip()

    books = Book.objects.all().order_by("id")

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        ).order_by("id")

    context = {
        "books": books,
        "search_query": search_query
    }
    return render(request, "book_details.html", context)


@login_required(login_url='login')
def book_summary(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book_summary.html", {"book": book})


@login_required(login_url='login')
def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        course = request.POST.get("course", "").strip()
        year = request.POST.get("year", "").strip()
        phone = request.POST.get("phone", "").strip()

        if not name or not email or not course or not year or not phone:
            messages.error(request, "All fields are required.")
            return render(request, "add_student.html")

        if Student.objects.filter(email=email).exists():
            messages.error(request, "A student with this email already exists.")
            return render(request, "add_student.html")

        Student.objects.create(
            name=name,
            email=email,
            course=course,
            year=year,
            phone=phone
        )

        messages.success(request, "Student added successfully.")
        return redirect("student_details")

    return render(request, "add_student.html")


@login_required(login_url='login')
def student_details(request):
    students = Student.objects.all().order_by("-id")
    return render(request, 'student_details.html', {'students': students})


def logout_view(request):
    logout(request)
    return redirect('login')