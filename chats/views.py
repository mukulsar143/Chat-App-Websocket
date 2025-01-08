from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import SupportTicket, TicketMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserRole
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SupportTicket, UserProfile, UserRole

@login_required(login_url="login")
def ticket_list(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render(request, "error.html", {"error": "UserProfile not found for the logged-in user."})

    role = user_profile.role  # Extract the role (Admin, Agent, or Customer)

    if role == UserRole.ADMIN:
        # Admin can see all tickets
        tickets = SupportTicket.objects.all()
        return render(request, "admin_tickets.html", {"tickets": tickets})
    
    elif role == UserRole.AGENT:
        # Agent can see only tickets assigned to them
        tickets = SupportTicket.objects.filter(assigned_agent=request.user)
        return render(request, "agent_tickets.html", {"tickets": tickets})
    
    elif role == UserRole.CUSTOMER:
        # Customer can see only their own tickets
        tickets = SupportTicket.objects.filter(customer=request.user)
        return render(request, "customer_tickets.html", {"tickets": tickets})
    
    else:
        return render(request, "error.html", {"error": "Invalid role."})



@login_required(login_url="login")
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    
    # Ensure access based on role
    if (request.role == "Customer" and ticket.customer != request.user) or (
        request.role == "Agent" and ticket.assigned_agent != request.user
    ):
        return redirect("ticket_list")

    messages = TicketMessage.objects.filter(ticket=ticket).order_by("created_at")
    return render(request, "ticket_details.html", {"ticket": ticket, "messages": messages})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")  # Role selected by the user

        # Validate passwords
        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already exists"})

        # Validate role
        if role not in [UserRole.AGENT, UserRole.CUSTOMER, UserRole.ADMIN]:
            return render(request, "register.html", {"error": "Invalid role selected"})

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create the user profile
        UserProfile.objects.create(user=user, role=role)

        return redirect("login")
    
    roles = [UserRole.AGENT, UserRole.CUSTOMER, UserRole.ADMIN]
    return render(request, "register.html", {"roles": roles})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("ticket_list")  # Redirect to tickets view
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def create_ticket(request):
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        message = request.POST.get('message')
        
        # Get the assigned agent
        assigned_agent = User.objects.get(id=request.POST.get('assigned_agent'))  # Assuming agent selection comes from the POST data
        
        # Create the ticket
        ticket = SupportTicket.objects.create(
            customer=request.user,  # The user creating the ticket is assumed to be a customer
            title=title,
            assigned_agent=assigned_agent
        )
        
        # Send the initial message to the assigned agent with the correct sender
        TicketMessage.objects.create(
            ticket=ticket,
            sender=request.user,  # This should be the current logged-in user (request.user)
        )
        print(request.user)

        # Redirect to the ticket detail page (adjust URL as necessary)
        return redirect('ticket_detail', ticket_id=ticket.id)

    # Fetch agents based on role (agents are users with 'Agent' role)
    agents = User.objects.filter(userprofile__role=UserRole.AGENT)

    # Pass agents to the template
    return render(request, 'create_ticket.html', {'agents': agents})