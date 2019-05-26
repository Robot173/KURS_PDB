from connection import connection
import psycopg2


class TestGateway:

    @staticmethod
    def create(requirements, title, device_id):
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
            query = 'INSERT INTO public.test(' \
                    '  requirements, title, device_id)' \
                    '  VALUES (ARRAY({%s}), %s, %s);'
            try:
                c.execute(query, (requirements, title, device_id))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0

    @staticmethod
    def read(search=None, value=None):
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
            query = 'SELECT * FROM public.test'
            if search is not None and value is not None:
                query += ' WHERE '
                if search is 'device':
                    query += 'device_id=%s;'
                if search is 'test':
                    query += 'test_id=%s;'
                if search is 'author':
                    query += 'device_id = ('\
                            'SELECT device_id FROM public.device '\
                            'WHERE author_id=%s)'
                if search is 'name_title':
                    query += 'device_id = ('\
                            'SELECT device_id FROM public.device '\
                            'WHERE name = %s)'
                c.execute(query, (value, ))
            else:
                query += ';'
                c.execute(query)
            connection.commit()
            return c.fetchall()

    @staticmethod
    def update(test_id, requirements, title, device_id):
        with connection.cursor() as c:
            query = 'UPDATE public.test' \
                    '  SET requirements=%s, title=%s, device_id=%s' \
                    '  WHERE test_id=%s;'
            c.execute(query, (requirements, title, device_id, test_id))
            connection.commit()
            return 1

    @staticmethod
    def delete(test_id):
        with connection.cursor() as c:
            query = 'DELETE FROM public.test WHERE test_id=%s;'
            try:
                c.execute(query, (test_id, ))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0
