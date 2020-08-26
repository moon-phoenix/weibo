import os
from hashlib import md5, sha256

from flask import session
from flask import redirect


# 对密码加密
def make_password(password):
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')
    hash_value = sha256(password).hexdigest()
    salt = os.urandom(16).hex()
    safe_password = salt + hash_value
    return safe_password


def check_password(password, safe_password):
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')
    hash_value = sha256(password).hexdigest()
    return hash_value == safe_password[32:]


def save_avatar(avatar_file):
    file_bin_data = avatar_file.stream.read()
    avatar_file.stream.seek(0)
    filename = md5(file_bin_data).hexdigest()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, 'static', 'upload', filename)
    avatar_file.save(filepath)
    avatar_url = f'/static/upload/{filename}'
    return avatar_url


def login_required(view_func):
    def check_session(*args, **kwargs):
        uid = session.get('uid')
        if not uid:
            return redirect('/user/login')
        else:
            return view_func(*args, **kwargs)

    return check_session
