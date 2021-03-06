from proxy.device_proxy import DeviceProxy as DevGW
from proxy.user_proxy import UserProxy as UsGW
from proxy.test_proxy import TestProxy as TestGW
from proxy.report_proxy import ReportProxy as RepGW
from proxy.rating_proxy import RatingProxy as RatGW
from proxy.post_proxy import PostProxy as PostGW
from constants import *
from exceptions import *
import datetime


class ServiceValidator:

    @staticmethod
    def validate_user(post):
        error = []
        if '@' not in post['email']:
            error.append('Почта указана без @')
        if post['password'] != post['password2']:
            error.append('Пароли не совпадают')
        if len(post['password']) < 5:
            error.append('Слишком короткий пароль')
        return error, post

    @staticmethod
    def validate_device(post):
        error = []
        if len(post['name']) < 5:
            error.append('Слишком короткое название устройства')
        if len(post['description']) < 10:
            error.append('Слишком короткое описание устройства')
        post.update({'image': '/blank.jpg'})
        return error, post

    @staticmethod
    def validate_post(post):
        error = []
        if len(post['title']) < 8:
            error.append('Слишком короткое название поста')
        if len(post['body']) < 10:
            error.append('Слишком короткая основная часть')
        if post['type'] not in POST_TYPES:
            error.append('Неверный тип поста')
        post['doc'] = datetime.datetime.now()
        return error, post

    @staticmethod
    def validate_test(post):
        error = []
        if len(post['requirements']) < 10:
            error.append('Слишком короткое описание теста')
        return error, post

    @staticmethod
    def validate_report(post):
        error = []
        if len(post['body']) < 20:
            error.append('Слишком короткий отчёт!')
        return error, post


class ServiceDB:
    @staticmethod
    def save_to_db(post, model, role):
        if model is 'user':
            res = UsGW.create(
                email=post['email'],
                password=post['password'],
                last_name=post['last_name'],
                first_name=post['first_name'],
                city=post['city'],
                profession=post['profession'],
                organization=post['organization'],
                dob=post['dob'],
                role=post['role'])
        elif model is 'device':
            res = DevGW.create(
                name=post['name'],
                description=post['description'],
                image=post['image'],
                author_id=post['user_id'],
                device_type=post['device_type'],
                role=role)
        elif model is 'test':
            res = TestGW.create(
                title=post['title'],
                requirements=post['requirements'],
                device_id=post['device_id'],
                role=role)
        elif model is 'post':
            res = PostGW.create(
                title=post['title'],
                annotation=post['annotation'],
                doc=post['doc'],
                body=post['body'],
                creator_id=post['creator_id'],
                post_type=post['post_type'],
                role=role)
        elif model is 'report':
            res = RepGW.create(
                tester_id=post['tester_id'],
                body=post['body'],
                test_id=post['test_id'],
                role=role)
        elif model is 'rating':
            res = RatGW.create(
                report_id=post['report_id'],
                developer_id=post['developer_id'],
                rating=post['rating'],
                comment=post['comment'],
                role=role)
        else:
            raise SaveException
        if res is 0:
            raise SaveException
        else:
            if res is -1:
                return 'No permission'
            return 'OK'
    
    @staticmethod
    def update_to_db(post, model, role):
        if model is 'user':
            res = UsGW.update(role,
                post['user_id'], post['email'], post['password'], post['last_name'], post['first_name'],
                post['city'], post['profession'], post['organization'], post['dob'], post['user_role'])
        elif model is 'device':
            res = DevGW.update(role,
                post['device_id'], post['user_id'], post['name'], post['description'],
                post['image'], post['device_type'])
        elif model is 'test':
            res = TestGW.update(role,
                post['test_id'], post['title'], post['requirements'], post['device_id'])
        elif model is 'post':
            res = PostGW.update(role,
                                post['post_id'], post['title'], post['annotation'], post['doc'], post['body'],
                                post['creator_id'], post['type'])
        elif model is 'report':
            res = RepGW.update(role, post['report_id'], post['tester_id'], post['body'], post['test_id'])
        elif model is 'rating':
            res = RatGW.update(role, post['rating_id'], post['report_id'],
                               post['developer_id'], post['rating'], post['comment'])
        else:
            raise UpdateException
        if res is 0:
            raise UpdateException
        elif res is -1:
            raise PermissionException
        else:
            return 'OK'
        
    @staticmethod
    def delete_object(post, model, role):
        if model is 'user':
            res = UsGW.delete(post['user_id'], role=role)
        elif model is 'device':
            res = DevGW.delete(post['device_id'], role=role)
        elif model is 'test':
            res = TestGW.delete(role, post['test_id'])
        elif model is 'post':
            res = PostGW.delete(post['post_id'], role=role)
        elif model is 'report':
            res = RepGW.delete(post['report_id'], role=role)
        elif model is 'rating':
            res = RatGW.delete(post['rating_id'], role=role)
        else:
            raise DeleteException
        if res is 0:
            raise DeleteException
        elif res is -1:
            raise PermissionException
        else:
            return 'OK'

    @staticmethod
    def get_objects(model, search=None, value=None):
        if model is 'user':
            res = UsGW.read(search, value)
        elif model is 'device':
            res = DevGW.read(search, value)
        elif model is 'test':
            res = TestGW.read(search, value)
        elif model is 'post':
            res = PostGW.read(search, value)
        elif model is 'report':
            res = RepGW.read(search, value)
        elif model is 'rating':
            res = RatGW.read(search, value)
        else:
            raise GetException
        return res


class ServiceOperations(ServiceDB, ServiceValidator):
    @staticmethod
    def registration(post, operation, role):
        model = 'user'
        if operation is 'add':
            error, post = ServiceValidator.validate_user(post)
            if len(error) == 0:
                try:
                    ServiceDB.save_to_db(post, model, role)
                except SaveException:
                    return 0, 'Произошла ошибка при регистрации'
                return 1, 'Регистрация прошла успешно'
            else:
                return 0, error
        if operation is 'edit':
            error, post = ServiceValidator.validate_user(post)
            if len(error) == 0:
                try:
                    ServiceDB.save_to_db(post, model, role)
                except SaveException:
                    return 0, 'Произошла ошибка при удалении'
                return 1, 'Регистрация прошла успешно'
            else:
                return 0, error
        if operation is 'delete':
            ServiceDB.delete_object(post, model, role)

    @staticmethod
    def post_management(operation, post, role):
        model = 'post'
        if operation is 'add':
            error, post = ServiceValidator.validate_post(post)
            if len(error) == 0:
                try:
                    ServiceOperations.save_to_db(post, model, role)
                except SaveException:
                    return 0, "Ошибка при сохранении"
                except PermissionException:
                    return 0, "Нету прав на выполнение операции"
                return 1, "Пост успешно добавлен"
            else:
                return 0, error
        if operation is 'edit':
            error, post = ServiceValidator.validate_post(post)
            if len(error) == 0:
                try:
                    ServiceOperations.update_to_db(post, model, role)
                except UpdateException:
                    return 0, "Ошибка при изменении"
                except PermissionException:
                    return 0, "Нету прав на выполнение операции"
                return 1, "Пост успешно изменен"
            else:
                return 0, error
        if operation is 'delete':
            try:
                ServiceDB.delete_object(post, model, role)
            except DeleteException:
                return 0, "Ошибка при удалении"
            except PermissionException:
                return 0, "Нету прав на выполнение операции"
            return 1, "Пост удален"

    @staticmethod
    def device_management(post, operation, role):
        model = 'device'
        if operation is 'add':
            error, post = ServiceValidator.validate_device(post)
            if len(error) == 0:
                try:
                    ServiceOperations.save_to_db(post, model, role)
                except SaveException:
                    return 0, "Ошибка при сохранении"
                except PermissionException:
                    return 0, "Нету прав на выполнение операции"
                return 1, "Устройство успешно добавлено"
            else:
                return 0, error
        if operation is 'edit':
            error, post = ServiceValidator.validate_device(post)
            if len(error) == 0:
                try:
                    ServiceOperations.update_to_db(post, model, role)
                except UpdateException:
                    return 0, "Ошибка при изменении"
                except PermissionException:
                    return 0, "Нету прав на выполнение операции"
                return 1, "Устройство успешно изменено"
            else:
                return 0, error
        if operation is 'delete':
            try:
                ServiceDB.delete_object(post, model, role)
            except DeleteException:
                return 0, "Ошибка при удалении"
            except PermissionException:
                return 0, "Нету прав на выполнение операции"
            return 1, "Устройство удалено"

    @staticmethod
    def test_management(post, operation, role):
        model = 'test'
        if operation is 'add':
            error, post = ServiceValidator.validate_test(post)
            if len(error) == 0:
                try:
                    ServiceOperations.save_to_db(post, model, role)
                except SaveException:
                    return 0, "Ошибка при сохранении"
                except PermissionException:
                    return 0, "Нету прав на выполнение операции"
                return 1, "Тест успешно добавлен"
            else:
                return 0, error
        if operation is 'edit':
            error, post = ServiceValidator.validate_test(post)
            if len(error) == 0:
                try:
                    ServiceOperations.update_to_db(post, model, role)
                except UpdateException:
                    return 0, "Ошибка при изменении"
                except PermissionException:
                    return 0, "Нету прав на выполнение операции"
                return 1, "Тест успешно изменен"
            else:
                return 0, error
        if operation is 'delete':
            try:
                ServiceDB.delete_object(post, model, role)
            except DeleteException:
                return 0, "Ошибка при удалении"
            except PermissionException:
                return 0, "Нету прав на выполнение операции"
            return 1, "Тест удален"

    @staticmethod
    def report_management(post, operation, role):
        model = 'report'
        if operation is 'add':
            error, post = ServiceValidator.validate_report(post)
            if len(error) == 0:
                try:
                    ServiceOperations.save_to_db(post, model, role)
                except SaveException:
                    return 0, "Ошибка при сохранении"
                except PermissionException:
                    return 0, "Нету прав на выполнение операции"
                return 1, "Отчёт успешно добавлен"
            else:
                return 0, error
        if operation is 'edit':
            error, post = ServiceValidator.validate_report(post)
            if len(error) == 0:
                try:
                    ServiceOperations.update_to_db(post, model, role)
                except UpdateException:
                    return 0, "Ошибка при изменении"
                except PermissionException:
                    return 0, "Нету прав на выполнение операции"
                return 1, "Отчёт успешно изменен"
            else:
                return 0, error
        if operation is 'delete':
            try:
                ServiceDB.delete_object(post, model, role)
            except DeleteException:
                return 0, "Ошибка при удалении"
            except PermissionException:
                return 0, "Нету прав на выполнение операции"
            return 1, "Отчёт удален"

    @staticmethod
    def rating_management(post, operation, role):
        model = 'rating'
        if operation is 'add':
            try:
                post['comment'] = 'none'
                ServiceOperations.save_to_db(post, model, role)
            except SaveException:
                return 0, "Ошибка при сохранении"
            except PermissionException:
                return 0, "Нету прав на выполнение операции"
            return 1, "Оценка успешно добавлена"
        if operation is 'edit':
            try:
                ServiceOperations.update_to_db(post, model, role)
            except UpdateException:
                return 0, "Ошибка при изменении"
            except PermissionException:
                return 0, "Нету прав на выполнение операции"
            return 1, "Оценка успешно изменена"
        if operation is 'delete':
            try:
                ServiceDB.delete_object(post, model, role)
            except DeleteException:
                return 0, "Ошибка при удалении"
            except PermissionException:
                return 0, "Нету прав на выполнение операции"
            return 1, "Оценка удалена"

    @staticmethod
    def find_specific_test(tests, title):
        for test in tests:
            if test['title'] == title:
                return 1, test
        return 0, "Нету теста"

    @staticmethod
    def read_devices_by_user():
        users = ServiceDB.get_objects('user', 'role', 'developer')
        for user in users:
            user['city'] = []
            devices = ServiceDB.get_objects('device', 'author_id', user['user_id'])
            for device in devices:
                device['author_id'] = []
                tests = ServiceDB.get_objects('test', 'device', device['device_id'])
                for test in tests:
                    device['author_id'].append(test)
            user['city'].append(device)
        return users


    @staticmethod
    def tests_with_reports(user_id):
        tests = ServiceDB.get_objects('test', 'author', user_id)
        for test in tests:
            test['device_id'] = []
            reports = ServiceDB.get_objects('report', 'test', test['test_id'])
            if reports != 0:
                for report in reports:
                    test['device_id'].append(report)
        return tests


class ServiceLayer():

    @staticmethod
    def add_user(email, password):
        result = UsGW.create(email, password)
        if result is 1:
            return "Успешно добавлен пользователь {}".format(email)
        else:
            return "Проблемы с добавлением пользователя"

    @staticmethod
    def get_users():
        result = UsGW.read()
        return result

    @staticmethod
    def get_user(id_user):
        result = UsGW.read(id_user)
        return result

    @staticmethod
    def verify_device(name, description, type_device):
        if len(description) < 10:
            return 'Описание: Слишком короткое описание'
        if len(description) > 300:
            return 'Описание: Слишком длинное описание'
        if len(name) < 4:
            return 'Название: Слишком короткое название'
        if len(name) > 30:
            return 'Название: Слишком длинное название'
        if len(type_device) < 4:
            return 'Тип устройства: Слишком короткий тип'
        if len(type_device) > 20:
            return 'Тип устройства: Слишком длинный тип'
        return 0

    @staticmethod
    def add_device(author_id, name, description, type_device):
        user = UsGW.read(author_id)
        if user is None:
            return "Устройство не было добавлено"
        result = UsGW.create(user[0][0], name, description, type_device)
        if result is 1:
            return "Успешно добавлено устройство {}".format(name)
        else:
            return "Проблемы с добавлением устройства"
        pass

    @staticmethod
    def change_device(id_device, author_id, name, description, type_device):
        DevGW.update(id_device, author_id, name, description, type_device)
        return "Успешно изменено устройство {}".format(name)

    @staticmethod
    def read_all_devices():
        return DevGW.read()

    @staticmethod
    def read_device(id_user):
        return DevGW.read("id", "{}".format(id_user))



    @staticmethod
    def delete_device(did):
        DevGW.delete(did)
        return "Успешно удалено устройство"
