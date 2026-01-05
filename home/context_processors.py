from user.models import SignupRecord

def user_role(request):
    """
    Context processor to add user role to all templates
    """
    role = None
    username = request.session.get("external_username")
    if username:
        try:
            user = SignupRecord.objects.get(username=username)
            role = user.role
        except SignupRecord.DoesNotExist:
            role = None
    return {'role': role}

