from django.conf import settings

def get_cloudinary_config():
    cloud_name = settings.CLOUDINARY_CLOUD_NAME
    api_key = settings.CLOUDINARY_API_KEY
    api_secret = settings.CLOUDINARY_API_SECRET

    if not cloud_name or not api_key or not api_secret:
        raise RuntimeError("Cloudinary env vars are missing")

    return cloud_name, api_key, api_secret