from connection import connection
import psycopg2


class UserGateway:

    @staticmethod
    def create(email, password, last_name, first_name, city, profession, organization, dob, role="tester"):
        with connection.cursor() as c:
            query = 'INSERT INTO public.tsr_user(' \
                    '  email, password, last_name, first_name, city, profession, organization, dob, role)' \
                    '  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
            try:
                c.execute(query, (email, password, last_name, first_name, city, profession, organization, dob, role))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0

    @staticmethod
    def read(search=None, value=None):
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
            query = 'SELECT * FROM public.tsr_user'
            if search is not None:
                if search is 'id':
                    query += ' WHERE user_id=%s'
                    c.execute(query, (value,))
                if search is 'email':
                    query += ' WHERE email=%s'
                    c.execute(query, (value,))
            else:
                query += ';'
                c.execute(query)
            return c.fetchall()

    @staticmethod
    def update(user_id, email, password, last_name, first_name, city, profession, organization, dob, role):
        with connection.cursor() as c:
            query = 'UPDATE public.tsr_user' \
                    '	SET email=%s, password=%s, last_name=%s,' \
                    '  first_name=%s, city=%s, profession=%s, organization=%s, dob=%s, role=%s' \
                    '	WHERE user_id=%s;'
            c.execute(query, (email, password, last_name, first_name, city, profession, organization, dob, role, user_id))
            connection.commit()
            return 1

    @staticmethod
    def delete(user_id):
        with connection.cursor() as c:
            query = 'DELETE FROM public.tsr_user WHERE user_id=%s;'
            try:
                c.execute(query, (user_id, ))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0
