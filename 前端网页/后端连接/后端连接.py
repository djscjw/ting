from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import timedelta
import mysql.connector


app = Flask(__name__, static_folder='E:/pycharm project/virtual_file/前端网页')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
CORS(app)
app.secret_key = 'your_secret_key'  # 设置一个密钥用于会话加密

# 连接到 MySQL 数据库
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="All_Information",
)


__email = []
__password = []
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    a = data.get('email')
    b = data.get('password')
    __email.append(a)
    __password.append(b)
    email = __email[-1]
    password = __password[-1]
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({'message': '登录成功'}), 200
    else:
        # 登录失败
        return jsonify({'message': '邮箱或密码错误'}), 401

@app.route('/get_user_id', methods=['GET'])
def get_user_id():
    email = __email[-1]
    cursor = db_connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cursor.fetchone()[0]
    session['user_id'] = user_id
    # 创建独立的数据库连接和游标对象
    db_connection_love = mysql.connector.connect(
     host="localhost",
    user="root",
    password="123456",
    database="Feedback",

    )
    if user_id:
        cursor = db_connection_love.cursor()
        cursor.execute("SELECT message FROM messages WHERE user_id = %s", (user_id,))
        message = cursor.fetchone()
        if message:
            return jsonify({'message': message[0]}), 200
        else:
            return jsonify({'message': '未找到消息'}), 404
        cursor.close()
        db_connection_love.close()
    else:
        return jsonify({'message': '用户未登录'}), 401


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    # 创建两个数据库连接和游标对象
    db_connection_feedback = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="Feedback",
    )
    db_connection_users = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="All_Information",
    )

    cursor_feedback = db_connection_feedback.cursor()
    cursor_users = db_connection_users.cursor()

    # 从请求中获取数据
    name = request.json['name']
    message = request.json['message']

    # 从users表获取id
    email = __email[-1]
    cursor_users.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id_result = cursor_users.fetchone()

    if user_id_result:
        user_id = user_id_result[0]

        # 检查feedback表中是否存在该id
        cursor_feedback.execute("SELECT id FROM feedback WHERE id = %s", (user_id,))
        feedback_exists = cursor_feedback.fetchone()

        if feedback_exists:
            # 如果存在该id，更新对应行的信息
            update_query = "UPDATE feedback SET name = %s, email = %s, message = %s WHERE id = %s"
            cursor_feedback.execute(update_query, (name, email, message, user_id))
        else:
            # 如果不存在，插入新行
            insert_query = "INSERT INTO feedback (id, name, email, message) VALUES (%s, %s, %s, %s)"
            cursor_feedback.execute(insert_query, (user_id, name, email, message))

        db_connection_feedback.commit()
        db_connection_users.commit()

    # 关闭游标和数据库连接
    cursor_feedback.close()
    cursor_users.close()

    return jsonify({'message': 'Feedback processed successfully'}), 200

@app.route('/login-developer', methods=['POST'])
def login_developer():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM developer WHERE email = %s AND password = %s", (email, password))
    developer = cursor.fetchone()

    if developer:
        # 开发者登录成功
        session['developer_logged_in'] = True  # 标记开发者已登录
        return jsonify({'message': '开发者登录成功'}), 200
    else:
        # 开发者登录失败
        return jsonify({'message': '开发者邮箱或密码错误'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        # 邮箱已经注册过
        return jsonify({'message': '该邮箱已注册'}), 400
    else:
        # 将新用户插入到数据库中
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        db_connection.commit()
        return jsonify({'message': '注册成功'}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

db_connection.close()

