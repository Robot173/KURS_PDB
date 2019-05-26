from gateway.device_gateway import DeviceGateway


class DeviceProxy:
    # Защищающий прокси
    @staticmethod
    def create(role, *args, **kwargs):
        if role is 'tester':
            return -1
        else:
            response = DeviceGateway.create(*args, **kwargs)
            return response

    @staticmethod
    def read(*args, **kwargs):
        response = DeviceGateway.read(*args, **kwargs)
        return response

    @staticmethod
    def update(role, *args, **kwargs):
        if role is 'tester':
            return -1
        else:
            response = DeviceGateway.update(*args, **kwargs)
            return response

    @staticmethod
    def delete(did, role):
        if role is 'tester':
            return -1
        else:
            response = DeviceGateway.delete(did)
            return response
