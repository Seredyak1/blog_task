"""blog_task URL Configuration
"""

from django.contrib import admin
from django.conf.urls import include, url

import debug_toolbar

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('blog.urls')),
]

urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
