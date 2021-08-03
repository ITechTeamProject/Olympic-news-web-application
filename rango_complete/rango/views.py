from django.db.models import query
from django.db.models.fields import SlugField
from django.shortcuts import render
from django.http import HttpResponse, response
import requests
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm, UserForm, UserProfileForm, UserRegistrationForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from rango.models import UserProfile,Team


def index(request):
    # return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    #request.session.set_test_cookie()

    visitor_cookie_handler(request)
    #context_dict['visits'] = request.session['visits']

    #Render the response and send it back!
    return render(request, 'rango/index.html', context=context_dict)

def team_index(request):

    visitor_cookie_handler(request)
    return render(request, 'rango/team_index.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:

        context_dict['category'] = None
        context_dict['pages'] = None

    # Search function code
    if request.method == 'POST':
        if request.method == 'POST':
            query = request.POST['query'].strip()

            if query:
                context_dict['result_list'] = run_query(query)
                context_dict['query'] = query
    
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method =='POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method =='POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def about(request):
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
    print(request.method)
    print(request.user)

    # if request.session.test_cookie_worked():
    #     print("TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()
    context_dict = {}
    context_dict['boldmessage'] = "This tutorial has been put together by Shijun Zhang."
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)

# def register(request):
#     registered = False

#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()

#             user.set_password(user.password)
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user

#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']

#             profile.save()

#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
        
#     else:
#         user_form =UserForm()
#         profile_form = UserProfileForm()

#     return render(request, 'rango/register.html', 
#                             context = {'user_form': user_form,
#                                        'profile_form': profile_form,
#                                        'registered': registered})

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect(reverse('rango:index'))
#             else:
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'rango/login.html')

# def some_view(request):
#     if not request.user.is_authenticated():
#         return HttpResponse("You are logged in.")
#     else:
#         return HttpResponse("You are not logged in.")

@login_required
def restricted(request):
    #return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, 'rango/restricted.html')

# @login_required
# def user_logout(request):
#     logout(request)

#     return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if(datetime.now() - last_visit_time).days >0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

# def search(request):
#     result_list = []

#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         if query:
#             result_list = run_query(query)

#     return render(request, 'rango/search.html', {'result_list': result_list})

class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserRegistrationForm()
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request):
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)
# @login_required
# def register_profile(request):
#     form = UserProfileForm()

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES)

#         if form.is_valid():
#             user_profile = form.save(commit=False)
#             user_profile.user = request.user
#             user_profile.save()

#             return redirect(reverse('rango:index'))

#         else:
#             print(form.errors)

#     context_dict = {'form': form}
#     return render(request, 'rango/profile_registration.html', context_dict)

class AboutView(View):
    def get(self, request):
        context_dict = {}

        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']

        return render(request, 'rango/about.html', context_dict)

class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})


    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))

        else:
            print(form.errors)

        return render(request, 'rango/add_category.html', {'form':form})


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'email': user_profile.email,
                                'picture': user_profile.picture})
        
        return (user, user_profile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:profile',
                                    kwargs={'username': username}))
        else:
            print(form.errors)
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango/profile.html', context_dict)

def get_category_list(max_results=0, starts_with=''):
    category_list = []

    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]

    return category_list

class CategorySuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''
        
        category_list = get_category_list(max_results=8, starts_with=suggestion)

        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')
        
        return render(request, 'rango/categories.html', {'categories': category_list})


# class LikeCategoryView(View):
#     @method_decorator(login_required)
#     def get(self, request):
#         category_id = request.GET['category_id']

#         try:
#             category = Category.objects.get(id=int(category_id))
#         except Category.DoesNotExist:
#             return HttpResponse(-1)
#         except ValueError:
#             return HttpResponse(-1)
        
#         category.likes = category.likes + 1
#         category.save()

#         return HttpResponse(category.likes)

class SearchAddPageView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET['category_id']
        title = request.GET['title']
        url = request.GET['url']

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse('Error - category not found.')
        except ValueError:
            return HttpResponse('Error - bad category ID.')
        
        p = Page.objects.get_or_create(category=category, 
                                        title=title, 
                                        url=url)

        pages = Page.objects.filter(category=category).order_by('-views')
        return render(request, 'rango/page_listing.html', {'pages': pages}) 

def goto_url(request):
    if request.method == 'GET':
        page_id = request.GET.get('page_id')

        try:
            selected_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))

        selected_page.views = selected_page.views + 1
        selected_page.save()

        return redirect(selected_page.url)
    
    return redirect(reverse('rango:index'))

@login_required
def team(request, category_name_slug):
    category_list = Category.objects.get(slug=category_name_slug)
    team_list = Team.objects.filter(name = category_list).order_by('-likes')#[:10]

    context_dict = {}
    #context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['sport'] = category_list
    context_dict['team'] = team_list
    return render(request, 'rango/team.html', context=context_dict) 

@login_required
def teamView(request):
    sport_list = Category.objects.order_by('-views')


    context_dict = {}
  
    context_dict['sport'] = sport_list
   
    return render(request, 'rango/teams.html', context=context_dict)

class VoteTeamsView(View):
    @method_decorator(login_required)
    def get(self, request):
        team_id = request.GET['team_id']
        try:
            team = Team.objects.get(id=int(team_id))
        except Team.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        team.likes = team.likes + 1
        team.save()
        return HttpResponse(team.likes)
