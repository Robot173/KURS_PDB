from connection import connection
import psycopg2


class PostGateway:

    @staticmethod
    def create(title, annotation, doc, body, creator_id, post_type):
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
            query = 'INSERT INTO public.post(' \
                    '  title, annotation, doc, body, creator_id, type)' \
                    '  VALUES (?, ?, ?, ?, ?, ?);'
            try:
                c.execute(query, (title, annotation, doc, body, creator_id, post_type))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0

    @staticmethod
    def read(search=None, value=None):
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
            query = 'SELECT * FROM public.post'
            if search is not None and value is not None:
                if search is 'id':
                    query += ' WHERE post_id=%s'
                    c.execute(query, (value, ))
            else:
                query += ' ORDER BY doc desc;'
                c.execute(query)
            connection.commit()
            return c.fetchall()

    @staticmethod
    def update(post_id, title, annotation, doc, body, creator_id, post_type):
        with connection.cursor() as c:
            query = 'UPDATE public.post' \
                    '	SET title=%s, annotation=%s, doc=%s, body=%s, creator_id=%s, type=%s' \
                    '	WHERE post_id=%s;'
            c.execute(query, (title, annotation, doc, body, creator_id, post_type, post_id))
            connection.commit()
            return 1

    @staticmethod
    def delete(post_id):
        with connection.cursor() as c:
            query = 'DELETE FROM public.post WHERE post_id=%s;'
            try:
                c.execute(query, (post_id, ))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0
