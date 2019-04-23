from connection import connection
import psycopg2


class ReportRatingGateway:

    @staticmethod
    def create(report_id, developer_id, rating, comment):
        with connection.cursor() as c:
            query = 'INSERT INTO public.report_rating(' \
                    '  report_id, developer_id, rating, comment)' \
                    '  VALUES (%s, %s, %s, %s);'
            try:
                c.execute(query, (report_id, developer_id, rating, comment))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0

    @staticmethod
    def read(search=None, value=None):
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
            query = 'SELECT * FROM public.report_rating'
            if search is not None and value is not None:
                if search is 'id':
                    query += ' WHERE rating_id=%s'
                    c.execute(query, (search, value, ))
                if search is 'report':
                    query += ' WHERE rating_id=%s'
                    c.execute(query, (search, value, ))
            else:
                query += ';'
                c.execute(query)
            connection.commit()
            return c.fetchall()

    @staticmethod
    def update(rating_id, report_id, developer_id, rating, comment):
        with connection.cursor() as c:
            query = 'UPDATE public.report_rating' \
                    '	SET report_id=%s, developer_id=%s, rating=%s, comment=%s' \
                    '	WHERE rating_id=%s;'
            c.execute(query, (report_id, developer_id, rating, comment, rating_id))
            connection.commit()
            return 1

    @staticmethod
    def delete(rid):
        with connection.cursor() as c:
            query = 'DELETE FROM public.rating WHERE rating_id=%s;'
            try:
                c.execute(query, (rid, ))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0
