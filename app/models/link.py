from app import get_db

def save(id, link):
  conn = get_db()
  with conn.cursor() as cur:
    cur.execute('INSERT INTO link (id, link) VALUES (%s, %s)', (id, link))
    conn.commit()

def all():
  conn = get_db()
  with conn.cursor() as cur:
    cur.execute('SELECT * FROM link')
    return cur.fetchall()

def get_link_by_key(id):
  conn = get_db()
  with conn.cursor() as cur:
    cur.execute('UPDATE link SET clicks=clicks + 1 WHERE id=%s', (id,))
    cur.execute('SELECT link FROM link WHERE id=%s', (id,))
    conn.commit()
    return cur.fetchone()
