def get_user_type(request):
    if request.user.is_authenticated:
        if request.user.groups.exists():
            return {"user_type": request.user.groups.first().name}
        return {"user_type": "Guest"}
    return {"user_type": "Guest"}
