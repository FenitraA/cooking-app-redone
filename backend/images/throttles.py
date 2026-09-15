from rest_framework.throttling import UserRateThrottle


class CloudinarySignRateThrottle(UserRateThrottle):
    scope = "cloudinary"
