from django.conf import settings


def google_analytics(request):
    """Adds the Google Analytics ID to the context"""
    return {"GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID}


def site_info(request):
    site_information = {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_DESCRIPTION": settings.SITE_DESCRIPTION,
    }
    return site_information
