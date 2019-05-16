from gateway.test_gateway import TestGateway


class TestProxy:
    # Защищающий прокси
    @staticmethod
    def create(role, *args, **kwargs):
        if role is 'tester':
            return -1
        else:
            response = TestGateway.create(*args, **kwargs)
            return response

    @staticmethod
    def read(*args, **kwargs):
        response = TestGateway.read(*args, **kwargs)
        return response

    @staticmethod
    def update(role, *args, **kwargs):
        if role is 'tester':
            return -1
        else:
            response = TestGateway.update(*args, **kwargs)
            return response

    @staticmethod
    def delete(role, *args, **kwargs):
        if role is 'tester':
            return -1
        else:
            response = TestGateway.delete(*args, **kwargs)
            return response
