# django/rest_framework imports
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from django.contrib import admin
from django.conf import settings

# project level imports
from accounts.users import views as account_views
from misc import views as misc_views
from libs.custom_api_docs import include_docs_urls
from clients import views as client_view
from candidate import views as candidate_view
from interview import views as interview_view



# intialize DefaultRouter
router = SimpleRouter()


# register misc app urls with router
router.register(r'', misc_views.APIConfViewSet, base_name='misc')

# register accounts app urls with router
router.register(r'accounts', account_views.UserViewSet, base_name='accounts')


# register clients app urls with router
router.register(r'clients', client_view.ClientViewSet, base_name='client')

# register job app urls with router
router.register(r'jd', client_view.JobViewSet, base_name='jd')

# register candidate app urls with router
router.register(r'candidate',candidate_view.CandidateViewSet,base_name='candidate')


router.register(r'interviews',interview_view.InterviewViewSet,base_name='interviews')

router.register(r'interviewsround',interview_view.InterviewRoundViewSet,base_name='interviews')

router.register(r'interviewsstatus',interview_view.InterviewStatusViewSet,base_name='interviews')




# router.register(r'candidate',candidate_view.CandidateViewSet,base_name='candidate')




# urlpatterns
urlpatterns = [
    path('api/v1/', include((router.urls, 'api'), namespace='v1')),
    path('HS456GAG4FAYJSTT0O/hire-admin/', admin.site.urls),
]

if settings.ENV != "PROD":
    urlpatterns += [re_path(r'^docs/A92DFFBB6B9EC/', include_docs_urls(title="Leads API"))]
