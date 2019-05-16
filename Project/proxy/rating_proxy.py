from gateway.report_rating_gateway import ReportRatingGateway


class RatingProxy:
    # Защищающий прокси
    @staticmethod
    def create(role, *args, **kwargs):
        if role is 'tester':
            return -1
        else:
            response = ReportRatingGateway.create(*args, **kwargs)
            return response

    @staticmethod
    def read(*args, **kwargs):
        response = ReportRatingGateway.read(*args, **kwargs)
        return response

    @staticmethod
    def update(role, *args, **kwargs):
        if role is 'tester':
            return -1
        else:
            response = ReportRatingGateway.update(*args, **kwargs)
            return response

    @staticmethod
    def delete(role, *args, **kwargs):
        if role is 'tester':
            return -1
        else:
            response = ReportRatingGateway.delete(*args, **kwargs)
            return response
