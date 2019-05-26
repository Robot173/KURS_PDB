from connection import connection
import psycopg2


class DeviceGateway:

    @staticmethod
    def create(name, description, image, author_id, device_type):
        with connection.cursor() as c:
            query = 'INSERT INTO public.device(' \
                    '  name, description, image, author_id, type)' \
                    '  VALUES (%s, %s, %s, %s, %s);'
            try:
                c.execute(query, (name, description, image, author_id, device_type))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0

    @staticmethod
    def read(search=None, value=None):
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
            query = 'SELECT * FROM public.device'
            if search is not None and value is not None:
                if search is 'id':
                    query += ' WHERE device_id=%s'
                    c.execute(query, (value,))
                if search is 'author_id':
                    query += ' WHERE author_id=%s'
                    c.execute(query, (value,))
            else:
                query += ';'
                c.execute(query)
            connection.commit()
            return c.fetchall()

    @staticmethod
    def update(device_id, author_id, name, description, image, device_type):
        with connection.cursor() as c:
            query = 'UPDATE public.device' \
                    '  SET name=%s, description=%s, image=%s, author_id=%s, type=%s' \
                    '  WHERE device_id=%s;'
            c.execute(query, (name, description, image, author_id, device_type, device_id))
            connection.commit()
            return 1

    @staticmethod
    def delete(did):
        with connection.cursor() as c:
            query = 'DELETE FROM public.device WHERE device_id=%s;'
            try:
                c.execute(query, (did, ))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0
