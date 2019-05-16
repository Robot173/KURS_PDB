from gateway.user_gateway import UserGateway


class TestProxy:
    # Защищающий прокси
    @staticmethod
    def create(*args, **kwargs):
        response = UserGateway.create(*args, **kwargs)
        return response

    @staticmethod
    def read(*args, **kwargs):
        response = UserGateway.read(*args, **kwargs)
        return response

    @staticmethod
    def update(role, *args, **kwargs):
        if role is not 'admin':
            return -1
        else:
            response = UserGateway.update(*args, **kwargs)
            return response

    @staticmethod
    def delete(role, *args, **kwargs):
        if role is not 'admin':
            return -1
        else:
            response = UserGateway.delete(*args, **kwargs)
            return response
