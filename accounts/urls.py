from django.urls import path

from .views import (
    LogInView, SignUpView, LogOutView, ChangePasswordView,
    RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView, LogOutConfirmView
)

app_name = 'accounts'

urlpatterns = [
    path('', LogInView.as_view(), name='log_in'),
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/confirm/', LogOutConfirmView.as_view(), name='log_out_confirm'),
    path('log-out/', LogOutView.as_view(), name='log_out'),

    path('sign-up/', SignUpView.as_view(), name='sign_up'),

    path('restore/password/', RestorePasswordView.as_view(), name='restore_password'),
    path('restore/password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
]


