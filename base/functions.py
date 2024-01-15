def clean_username(self):
    username = self.cleaned_data['username']
    if ' ' in username:
        print("username got a space of it  ")
        messages.error(  "username got a space of it ")
    return redirect(request, 'home') 
def clean_email(self ):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists(email):
        print("email is already in use")
        messages.error( "email is already in use")
    return redirect(request, 'home') 