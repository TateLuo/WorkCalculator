import base64
with open('icon.png', 'rb') as icon:
    icon_str = base64.b64encode(icon.read())
    icon_bytes = 'icon_bytes = ' + str(icon_str)
with open('icon.py', 'w+') as icon_py:
    icon_py.write(icon_bytes)