from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__, static_folder='E:/pycharm project/virtual_file/前端网页')
CORS(app)

# 连接到 MySQL 数据库
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="Feedback",
)

# 创建全局游标对象
global_cursor = db_connection.cursor()

# 定义路由，获取所有反馈信息并提供给前端
@app.route('/feedback', methods=['GET'])
def get_feedback():
    db_connection.commit()
    global_cursor.execute('SELECT id, name, email, created_at FROM feedback ORDER BY id;')
    feedback_data = global_cursor.fetchall()
    feedback_list = []
    for feedback in feedback_data:
        feedback_dict = {
            'id': feedback[0],
            'name': feedback[1],
            'email': feedback[2],
            'created_at': feedback[3].strftime("%Y-%m-%d %H:%M:%S")
        }
        feedback_list.append(feedback_dict)
    db_connection.commit()
    return jsonify(feedback_list)

# 定义路由，获取特定消息内容
@app.route('/message/<int:id>', methods=['GET'])
def get_message(id):
    # 创建独立的数据库连接和游标对象
    db_connection_message = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="Feedback",
    )
    cursor = db_connection_message.cursor()

    cursor.execute('SELECT message FROM feedback WHERE id = %s', (id,))
    message = cursor.fetchone()

    # 关闭游标和数据库连接
    cursor.close()
    db_connection_message.close()

    return jsonify({'message': message[0]}) if message else jsonify({'message': 'Message not found'}), 200


@app.route('/send_message', methods=['POST'])
def send_message():
    # 从请求中获取管理员发送的消息和指定用户的ID
    message = request.json['message']
    user_id = request.json['user_id']

    # 删除数据库中已存在的相同 user_id 记录
    cursor = db_connection.cursor()
    delete_query = 'DELETE FROM messages WHERE user_id = %s'
    cursor.execute(delete_query, (user_id,))

    # 将新消息插入到数据库中
    insert_query = 'INSERT INTO messages (user_id, message) VALUES (%s, %s)'
    cursor.execute(insert_query, (user_id, message))

    db_connection.commit()
    cursor.close()
    return jsonify({'message': 'Message sent successfully'}), 200

if __name__ == '__main__':
    # 运行Flask程序
    app.run(port=5001, debug=True)

# 关闭全局游标和数据库连接
global_cursor.close()
db_connection.close()