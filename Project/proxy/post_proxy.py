from gateway.post_gateway import PostGateway


class TestProxy:
    # Защищающий прокси
    @staticmethod
    def create(role='none', *args, **kwargs):
        if role is 'none':
            return -1
        else:
            response = PostGateway.create(*args, **kwargs)
            return response

    @staticmethod
    def read(*args, **kwargs):
        response = PostGateway.read(*args, **kwargs)
        return response

    @staticmethod
    def update(role='none', *args, **kwargs):
        if role is 'none':
            return -1
        else:
            response = PostGateway.update(*args, **kwargs)
            return response

    @staticmethod
    def delete(role='none', *args, **kwargs):
        if role is 'none':
            return -1
        else:
            response = PostGateway.delete(*args, **kwargs)
            return response
