from rest_framework import renderers
import json
from rest_framework.exceptions import APIException


# In your UserRenderer class
class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if isinstance(data, APIException):
            response = {'errors': data.detail}
        else:
            response = data
        # Use the super().render() method without json.dumps
        return super().render(response, accepted_media_type, renderer_context)

# new ------
# from rest_framework import renderers
# import json


# class UserRenderer(renderers.BrowsableAPIRenderer):
#     charset = 'utf-8'
#     # Add the media type attribute
#     media_type = 'application/json'

#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         response = ''
#         if 'ErrorDetail' in str(data):
#             response = json.dumps({'errors': data})
#         else:
#             response = json.dumps(data)
#         return super().render(response, accepted_media_type, renderer_context)
