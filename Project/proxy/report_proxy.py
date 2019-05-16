from gateway.report_gateway import ReportGateway


class ReportProxy:
    # Защищающий прокси
    @staticmethod
    def create(role, *args, **kwargs):
        if role is 'developer':
            return -1
        else:
            response = ReportGateway.create(*args, **kwargs)
            return response

    @staticmethod
    def read(*args, **kwargs):
        response = ReportGateway.read(*args, **kwargs)
        return response

    @staticmethod
    def update(role, *args, **kwargs):
        if role is 'developer':
            return -1
        else:
            response = ReportGateway.update(*args, **kwargs)
            return response

    @staticmethod
    def delete(role, *args, **kwargs):
        if role is 'developer':
            return -1
        else:
            response = ReportGateway.delete(*args, **kwargs)
            return response