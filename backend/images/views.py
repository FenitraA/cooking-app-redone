import time

import cloudinary
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from images.services import get_cloudinary_config
from images.throttles import CloudinarySignRateThrottle

class CloudinarySignView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [CloudinarySignRateThrottle]

    def get(self, request):
        folder = request.query_params.get("folder", "lots")

        try:
            cloud_name, api_key, api_secret = get_cloudinary_config()
        except RuntimeError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        timestamp = int(time.time())

        params_to_sign = {
            "timestamp": timestamp,
            "folder": folder,
        }

        signature = cloudinary.utils.api_sign_request(
            params_to_sign,
            api_secret,
        )

        return Response(
            {
                "cloudName": cloud_name,
                "apiKey": api_key,
                "timestamp": timestamp,
                "signature": signature,
                "folder": folder,
            }
        )
