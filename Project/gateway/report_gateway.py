from connection import connection
import psycopg2


class ReportGateway:

    @staticmethod
    def create(tester_id, body, test_id):
        with connection.cursor() as c:
            query = 'INSERT INTO public.report(' \
                    '  tester_id, body, test_id)' \
                    '  VALUES (%s, %s, %s);'
            try:
                c.execute(query, (tester_id, body, test_id))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0

    @staticmethod
    def read(search=None, value=None):
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
            query = 'SELECT * FROM public.report'
            if search is not None and value is not None:
                if search is 'id':
                    query += ' WHERE report_id=%s'
                    c.execute(query, (value, ))
                if search is 'test':
                    query += ' WHERE test_id=%s'
                    try:
                        c.execute(query, (value, ))
                    except psycopg2.DatabaseError:
                        return 0
            else:
                query += ';'
                c.execute(query)
            connection.commit()
            return c.fetchall()

    @staticmethod
    def update(report_id, tester_id, body, test_id):
        with connection.cursor() as c:
            query = 'UPDATE public.report' \
                    '	SET body=%s, test_id=%s, tester_id=%s' \
                    '	WHERE report_id=%s;'
            c.execute(query, (tester_id, body, test_id, report_id))
            connection.commit()
            return 1

    @staticmethod
    def delete(report_id):
        with connection.cursor() as c:
            query = 'DELETE FROM public.report WHERE report_id=%s;'
            try:
                c.execute(query, (report_id, ))
                connection.commit()
                return 1
            except psycopg2.DatabaseError:
                return 0
