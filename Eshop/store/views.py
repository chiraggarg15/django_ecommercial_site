from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from .models.product import Product
from .models.categories import Categories
from .models.customer import Customer
from django.views import View

# Create your views here.
# when ever we are renderinging the html page in that time we have to pass the data from database in dictonary form
class Index(View):
        def get(self,request):
                cart=request.session.get('cart')
                if not cart:
                        request.session['cart']={}
                products =None
                categories=Categories.get_all_categories()
                # print(categories)
                categoryID = request.GET.get('category')
                if categoryID:
                        products=Product.objects.filter(category=categoryID)
                else:
                        products=Product.objects.all()
                data ={}
                data['products']=products
                data['categories']=categories
                print('you are:',request.session.get('email'))
                return render(request,'index.html',data)     
        def post(self,request):
                product=request.POST.get('product')
                remove=request.POST.get('remove')
                cart=request.session.get('cart')
                if cart:
                        quantity = cart.get(product)
                        if quantity:
                                if remove:
                                        if quantity <= 1:
                                                cart.pop(product)
                                        else:
                                                cart[product] =quantity-1
                                else:
                                        cart[product] =1+quantity
                        else:
                                cart[product]=1
                else:
                        cart={}
                        cart[product]=1
                request.session['cart']=cart
                print(request.session['cart'])
                return redirect('homepage')
def sign(request):
        if request.method == 'GET':
                return render(request,'signup.html')
        else:
                PostData = request.POST
                first_name=PostData.get('firstname')
                last_name=PostData.get('lastname')
                phone=PostData.get('phone')
                email=PostData.get('email')
                password=PostData.get('password')

                #validate
                values={
                        'first_name':first_name,
                        'last_name':last_name,
                        'phone_number':phone,
                        'email':email
                }
                error_message = None
                if(not first_name):
                        error_message="first Name required !!"
                elif len(first_name)<4:
                                error_message='first_name should be equal to or greater then 4 '
                
                if  not error_message:
                        print(first_name,last_name,phone,email,password)
                        customer =Customer(
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone,
                        email=email,
                        password=password
                        )
                        customer.password=make_password(customer.password)
                        customer.register()
                        return redirect('homepage')
                else:
                        data={
                                'error':error_message,
                                'values':values
                        }  
                        return render(request,'signup.html',data)
                
class Login(View):
        def get(self,request):
                return render(request,'login.html')
        def post(self,request):
                email =request.POST.get('email')
                password=request.POST.get('password')
                customer = Customer.get_customer_by_email(email)
                error_message = None
                if customer:
                        flag = check_password(password,customer.password)
                        print("flag " ,flag)
                        if flag:
                                request.session['customer_id']=customer.id
                                request.session['email']=customer.email
                                return redirect('homepage')
                        else:
                                error_message='Email or password invlaid !!'
                else:
                        error_message='Email or password invlaid !!'
                print(customer)
                return render(request,'login.html',{'error':error_message})