from django.urls import re_path
from .views import CustomerAddView, CustomerDelView, CustomerEditView, CustomerListView, PaymentAddView, PaymentDelView, PaymentEditView, PaymentListView, LoginView


urlpatterns = [

    re_path(r'^customer/list/$', CustomerListView.as_view(), name="customer_list"),
    re_path(r'^customer/add/$', CustomerAddView.as_view(), name="customer_add"),
    re_path(r'^customer/edit/(?P<cid>\d+)/$', CustomerEditView.as_view(), name="customer_edit"),
    re_path(r'^customer/del/(?P<cid>\d+)/$', CustomerDelView.as_view(), name="customer_del"),
    # re_path(r'^customer/import/$', customer.customer_import),
    # re_path(r'^customer/tpl/$', customer.customer_tpl),
    #
    re_path(r'^payment/list/$', PaymentListView.as_view(), name="payment_list"),
    re_path(r'^payment/add/$', PaymentAddView.as_view(), name="payment_add"),
    re_path(r'^payment/edit/(?P<pid>\d+)/$', PaymentEditView.as_view(), name="payment_edit"),
    re_path(r'^payment/del/(?P<pid>\d+)/$', PaymentDelView.as_view(), name="payment_del"),
    re_path(r'^login/$', LoginView.as_view(), name="login"),
]