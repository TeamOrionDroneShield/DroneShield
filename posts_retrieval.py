import json
import sqlite3


def posts_retrieving():
    print("ciao")
    conn = sqlite3.connect(r"./socialdb.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM POST ''')
    conn.commit()
    data = c.fetchall()
    conn.close()
    jsondata = dict()
    posts = []
    jsondata['posts'] = posts
    for post in data:
        post_data = dict()
        post_data['id'] = post[1]
        post_data['title'] = post[2]
        post_data['date'] = post[3]
        posts.append(post_data)

    return str(json.dumps(jsondata))
