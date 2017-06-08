from collections import namedtuple

import psycopg2

from pyredispg.exceptions import RedisWrongTypeException
from pyredispg.models import EntryKey, KeyValue


class PostgresDao(object):
    TYPE_GLOBAL = 1
    TYPE_HASH = 2
    TYPE_SET = 3
    TYPE_ZSET = 4

    TYPE_STRING_MAP = {
        TYPE_GLOBAL: 'string',
        TYPE_HASH: 'hash',
        TYPE_SET: 'set',
        TYPE_ZSET: 'zset'
    }

    def __init__(self, config):
        self._conn = psycopg2.connect(**config)
        self._conn.autocommit = False

    def __del__(self):
        self._conn.close()

    def _create_key(self, cursor, db, key, key_type):
        cursor.execute('INSERT INTO key_entries (db, skey, id, key_type) VALUES (%(db)s, %(skey)s, %(id)s, %(key_type)s)',
                       {
                           'db': db,
                           'skey': key,
                           'key_type': key_type
                       })

    def _get_entry_key(self, db, key):
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT id, key_type FROM key_entries WHERE db=%s AND skey=%s", (db, key,))
            row = cursor.fetchone()
            return EntryKey(row[0], row[1]) if row else None

    def _get_id(self, db, key, key_type, create=False):
        entry_key = self._get_entry_key(db, key)
        if entry_key is None:
            return self._add_key(db, key, key_type) if create else None
        elif entry_key.key_type != key_type:
            raise RedisWrongTypeException('Operation against a key holding the wrong kind of value')
        else:
            return entry_key.id

    def _get_set_element_ids(self, db, values):
        with self._conn.cursor() as cursor:
            query = """
                SELECT id, skey FROM set_element_lookup
                WHERE skey IN %(values)s
                AND db=%(db)s
            """

            cursor.execute(query, {'values': tuple(values), 'db': db})
            rows = cursor.fetchall()
            existing_ids = [row[0] for row in rows]
            existing_skeys = [row[1] for row in rows]
            print existing_ids

            if set(existing_skeys) != set(values):
                query = """
                    INSERT INTO set_element_lookup(db, skey)
                    VALUES {values}
                    ON CONFLICT (db, skey)
                    DO UPDATE
                      SET skey=excluded.skey
                    WHERE set_element_lookup.skey <> excluded.skey
                    RETURNING id
                """.format(
                    values=','.join(["({db}, '{v}')".format(db=db, v=v) for v in set(values) - set(existing_skeys)])
                )
                cursor.execute(query)
                return existing_ids + [element_id for [element_id] in cursor.fetchall()]
            else:
                return existing_ids

    def delete(self, db, key):
        with self._conn.cursor() as cursor:
            cursor.execute("DELETE FROM key_entries WHERE db=%s AND skey=%s", (db, key,))
            return cursor.rowcount

    def exists(self, db, key):
        return self.type(db, key) is not None

    def get(self, db, key):
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT value FROM global_hashmap JOIN key_entries USING (id) WHERE db=%s AND skey=%s", (db, key,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None

    def mget(self, db, keys):
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT skey, value FROM global_hashmap JOIN key_entries USING (id) WHERE db=%(db)s AND skey IN %(keys)s", {'db': db, 'keys': tuple(keys)})
            row_dict = dict([(row[0], row[1]) for row in cursor])
            return [row_dict.get(key) for key in keys]

    def get_keys(self, db, pattern):
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT skey FROM key_entries WHERE db=%s AND skey ILIKE %s", (db, pattern.replace('*', '%'),))
            return [key for [key] in cursor]

    def dbsize(self):
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(1) FROM key_entries")
            row = cursor.fetchone()
            return row[0] if row else 0

    def delete_all_dbs(self):
        with self._conn.cursor() as cursor:
            cursor.execute("TRUNCATE key_entries")
            cursor.execute("TRUNCATE set_element_lookup")
        self._conn.commit()

    def delete_db(self, db):
        with self._conn.cursor() as cursor:
            cursor.execute("DELETE FROM key_entries WHERE db=%(db)s", {'db': db})
            cursor.execute("DELETE FROM set_element_lookup WHERE db=%(db)s", {'db': db})
        self._conn.commit()

    def _add_key(self, db, key, key_type):
        with self._conn.cursor() as cursor:
            query = """
                INSERT INTO key_entries (db, skey, key_type)
                VALUES (%(db)s, %(skey)s, %(key_type)s)
                RETURNING id
            """
            cursor.execute(query, {
                'db': db,
                'skey': key,
                'key_type': key_type
            })
            [row_id] = cursor.fetchone()
            return row_id

    def hset(self, db, key, hkey, value):
        row_id = self._get_id(db, key, self.TYPE_HASH, True)

        with self._conn.cursor() as cursor:
            query = """
                INSERT INTO hashmap (id, hkey, value)
                VALUES (%(id)s, %(hkey)s, %(value)s)
                ON CONFLICT (id, hkey)
                DO UPDATE
                  SET value = excluded.value
                  WHERE excluded.value <> hashmap.value
            """
            cursor.execute(query, {
                'id': row_id,
                'hkey': hkey,
                'value': value
            })
            row_count = cursor.rowcount

        self._conn.commit()
        return row_count

    def hget(self, db, key, hkey):
        row_id = self._get_id(db, key, self.TYPE_HASH)

        with self._conn.cursor() as cursor:
            query = """
                SELECT value
                FROM hashmap
                WHERE
                  id = %(id)s AND
                  hkey = %(hkey)s
            """
            cursor.execute(query, {
                'id': row_id,
                'hkey': hkey
            })
            row = cursor.fetchone()
            return row[0] if row else None

    def hmget(self, db, key, hkeys):
        row_id = self._get_id(db, key, self.TYPE_HASH)

        with self._conn.cursor() as cursor:
            query = """
                SELECT hkey, value
                FROM hashmap
                WHERE
                  id = %(id)s AND
                  hkey IN %(hkeys)s
            """
            cursor.execute(query, {
                'id': row_id,
                'hkeys': tuple(hkeys)
            })
            row_by_hkey = dict([(row[0], row[1]) for row in cursor.fetchall()])
            return [row_by_hkey.get(hkey) for hkey in hkeys]

    def hexists(self, db, key, hkey):
        row_id = self._get_id(db, key, self.TYPE_HASH)

        with self._conn.cursor() as cursor:
            query = """
                SELECT 1
                FROM hashmap
                WHERE
                  id = %(id)s AND 
                  hkey = %(hkey)s
            """
            cursor.execute(query, {
                'id': row_id,
                'hkey': hkey
            })
            row = cursor.fetchone()
            return row is not None

    def hdel(self, db, key, hkey):
        row_id = self._get_id(db, key, self.TYPE_HASH)

        with self._conn.cursor() as cursor:
            query = """
                DELETE FROM hashmap
                WHERE
                  id = %(id)s AND 
                  hkey = %(hkey)s
            """
            cursor.execute(query, {
                'id': row_id,
                'hkey': hkey
            })
            return cursor.rowcount == 1

    def hgetall(self, db, key):
        row_id = self._get_id(db, key, self.TYPE_HASH)

        with self._conn.cursor() as cursor:
            query = """
                SELECT hkey, value
                FROM hashmap
                WHERE
                  id = %(id)s
            """
            cursor.execute(query, {
                'id': row_id,
            })
            return [KeyValue(row[0], row[1]) for row in cursor]

    def hkeys(self, db, key):
        row_id = self._get_id(db, key, self.TYPE_HASH)

        with self._conn.cursor() as cursor:
            query = """
                SELECT hkey
                FROM hashmap
                WHERE
                  id = %(id)s
            """
            cursor.execute(query, {
                'id': row_id,
            })
            return [row[0] for row in cursor]

    def hmset(self, db, key, key_values):
        row_id = self._get_id(db, key, self.TYPE_HASH, True)

        with self._conn.cursor() as cursor:
            query = """
                INSERT INTO hashmap (id, hkey, value)
                VALUES {values}
                ON CONFLICT (id, hkey)
                DO UPDATE
                  SET value = excluded.value
                  WHERE excluded.value <> hashmap.value
            """.format(
                values = ','.join(["({id}, '{hkey}', '{value}')".format(id=row_id, hkey=kv.key, value=kv.value) for kv in key_values])
            )
            cursor.execute(query)
            row_count = cursor.rowcount

        self._conn.commit()
        return row_count

    def hvals(self, db, key):
        row_id = self._get_id(db, key, self.TYPE_HASH)

        with self._conn.cursor() as cursor:
            query = """
                SELECT value
                FROM hashmap
                WHERE
                  id = %(id)s
            """
            cursor.execute(query, {
                'id': row_id,
            })
            return [row[0] for row in cursor]

    def hlen(self, db, key):
        row_id = self._get_id(db, key, self.TYPE_HASH)

        with self._conn.cursor() as cursor:
            query = """
                SELECT COUNT(1)
                FROM hashmap
                WHERE
                  id = %(id)s
            """
            cursor.execute(query, {
                'id': row_id,
            })
            row = cursor.fetchone()
            return int(row[0]) if row else 0

    def persist(self, db, key):
        row_id = self._get_id(db, key, self.TYPE_GLOBAL)
        with self._conn.cursor() as cursor:
            cursor.execute("UPDATE global_hashmap SET expiration_date=NULL WHERE id=%(id)s AND expiration_date IS NOT NULL", {'id': row_id})
            return cursor.rowcount

    def sadd(self, db, key, values):
        row_id = self._get_id(db, key, self.TYPE_SET, True)
        element_ids = self._get_set_element_ids(db, values)
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT ICOUNT(elements) FROM set_hashmap WHERE id=%(id)s', {'id': row_id})
            row = cursor.fetchone()
            old_element_count = row[0] if row else 0
            print old_element_count
            query = """
                INSERT INTO set_hashmap(id, elements)
                VALUES (%(id)s, %(elements)s)
                ON CONFLICT (id)
                DO UPDATE
                  SET elements = UNIQ(SORT(excluded.elements + set_hashmap.elements))
                RETURNING ICOUNT(elements)
            """

            cursor.execute(query, {
                'id': row_id,
                'elements': element_ids
            })
            [new_element_count] = cursor.fetchone()
        self._conn.commit()
        return new_element_count - old_element_count

    def smembers(self, db, key):
        row_id = self._get_id(db, key, self.TYPE_SET)
        with self._conn.cursor() as cursor:
            query = """
                SELECT
                    skey
                FROM
                    (SELECT UNNEST(elements) AS id FROM set_hashmap WHERE id=%(id)s) a
                    JOIN set_element_lookup b USING (id)
                    WHERE db=%(db)s
            """
            cursor.execute(query, {'id': row_id, 'db': db})
            return [skey for [skey] in cursor.fetchall()]

    def scard(self, db, key):
        row_id = self._get_id(db, key, self.TYPE_SET)
        with self._conn.cursor() as cursor:
            query = """
                SELECT ICOUNT(elements)
                FROM set_hashmap
                WHERE id=%(id)s
            """
            cursor.execute(query, {'id': row_id})
            row = cursor.fetchone()
            return row[0] if row else 0

    def set(self, db, key, value, ex=None, mx=None, overwrite=True):
        if self.exists(db, key):
            self.delete(db, key)
        row_id = self._add_key(db, key, self.TYPE_GLOBAL)

        with self._conn.cursor() as cursor:
            query = """
                INSERT INTO global_hashmap(id, value, expiration_date)
                VALUES (%(id)s, %(value)s, %(expiration_date)s)
            """
            cursor.execute(query, {
                'id': row_id,
                'value': value,
                'expiration_date': '2020-01-01'
            })
        self._conn.commit()

    def type(self, db, key):
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT key_type FROM key_entries WHERE db=%s AND skey=%s", (db, key,))
            row = cursor.fetchone()
            return row[0] if row else None


    def type_str(self, db, key):
        t = self.type(db, key)
        return self.TYPE_STRING_MAP[t] if t else None
