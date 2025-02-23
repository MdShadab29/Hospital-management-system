# from django.shortcuts import redirect
# from django.utils.deprecation import MiddlewareMixin
# from django.contrib.auth import logout

# '''
#     This is a middleware class used for checking if the user is authenticated or not.

#     Some other logics are implemented here
# '''

# class AuthMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         user = request.user
#         if '/login/' in request.path:
#             return None
#         if '/about/' in request.path:
#             return None
#         if '/appointment/' in request.path:
#             if user and user.is_authenticated and user.is_admin:
#                return None
            
#             else:
#                 if user and user.is_authenticated:
#                     logout(request)
#                 return redirect('login')
#         if '/doctor/' in request.path:
#             if user and user.is_authenticated and user.is_doctor:
#                return None
            
#             else:
#                 if user and user.is_authenticated:
#                     logout(request)
#                 return redirect('login')

#         if '/patient/signup' in request.path:
#             return None
#         if '/patient/' in request.path:
#             if user and user.is_authenticated and user.is_patient:
#                return None
            
#             else:
#                 if user and user.is_authenticated:
#                     logout(request)
#                 return redirect('login')
