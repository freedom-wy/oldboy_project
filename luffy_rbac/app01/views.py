from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Customer, Payment
from rbac.models import UserInfo
from .forms import CustomerForm, PaymentForm, PaymentUserForm
from django.http import HttpResponse
from rbac.service.init_permission import init_permission


class CustomerListView(View):
    def get(self, request):
        # 查询所有客户信息
        data_list = Customer.objects.all()
        return render(request, "customer_list.html", {"data_list": data_list})


class CustomerAddView(View):
    def get(self, request):
        """
        添加客户信息
        """
        form = CustomerForm()
        return render(request, "customer_add.html", {"form": form})

    def post(self, request):
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customer/list/')
        return render(request, 'customer_add.html', {'form': form})


class CustomerEditView(View):
    """
    编辑客户信息
    """

    def get(self, request, cid):
        obj = Customer.objects.get(id=cid)
        form = CustomerForm(instance=obj)
        return render(request, "customer_edit.html", {"form": form})

    def post(self, request, cid):
        obj = Customer.objects.get(id=cid)
        form = CustomerForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/customer/list/')
        return render(request, 'customer_edit.html', {'form': form})


class CustomerDelView(View):
    def get(self, request, cid):
        # 获取id
        Customer.objects.filter(id=cid).delete()
        return redirect("/customer/list/")


class PaymentListView(View):
    """
    付费列表
    """
    def get(self, request):
        data_list = Payment.objects.all()
        return render(request, "payment_list.html", {"data_list":data_list})


class PaymentAddView(View):
    """
    添加账单
    """
    def get(self, request):
        form = PaymentForm()
        return render(request, "payment_add.html", {"form": form})

    def post(self, request):
        form = PaymentForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/payment/list/")
        return render(request, "payment_add.html", {"form": form})


class PaymentEditView(View):
    def get(self, request, pid):
        obj = Payment.objects.get(id=pid)
        form = PaymentForm(instance=obj)
        return render(request, 'payment_edit.html', {'form': form})

    def post(self, request, pid):
        obj = Payment.objects.get(id=pid)
        form = PaymentForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/payment/list/')
        return render(request, 'payment_edit.html', {'form': form})


class PaymentDelView(View):
    def get(self, request, pid):
        Payment.objects.filter(id=pid).delete()
        return redirect('/payment/list/')


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        # 获取登录的用户名密码
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        # 查库
        current_user = UserInfo.objects.filter(name=user, password=pwd).first()
        if not current_user:
            return render(request, "login.html", {"msg": "用户名或密码错误"})
        # 将用户信息放入session
        request.session["user_info"] = {"id": current_user.id, "name": current_user.name}
        # 登录后初始化权限
        init_permission(current_user, request)
        return redirect("/customer/list")
