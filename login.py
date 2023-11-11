def register():
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    if register_check(new_username) :
        return f'<script> alert("نام کاربری شما از قبل در سیستم وجود دارد") </script>'
    else :    
        with open('users.txt', 'a') as file:
            file.write(f'{new_username},{new_password}\n')
        return f'<script> alert("{new_username} عزیز  ثبت نام شما با موفقیت انجام شد  ") </script>'
        