from ServiceLayer import ServiceValidator, ServiceDB
post = {'name': 'Устройство', 'description': 'Описание описания', 'image': 'img', 'creator_id': 1, 'post_type': 'Компьютер'}
# post2 = {'email': 'email', 'password': 'ps', 'password2': 'ps'}
# error, device = ServiceValidator.validate_device(post)
# if len(error) is not 0:
#     print(error)
# else:
#     print(device['name'])
# error2, user = ServiceValidator.validate_user(post2)
# if len(error2) is not 0:
#     print(error2)
ServiceDB.save_to_db(post, 'device')
