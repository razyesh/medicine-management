def get_user_type(request):
    print(request.user.groups.first().name)
    return {"user_type": request.user.groups.first().name}