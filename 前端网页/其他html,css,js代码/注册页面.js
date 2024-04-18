document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单默认提交行为

        // 获取表单中的邮箱和密码
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        // 检查两次输入的密码是否一致
        if (password !== confirmPassword) {
            alert("两次输入的密码不一致，请重新输入！");
            return;
        }

        // 构造发送给后端的数据
        const data = {
            email: email,
            password: password
        };

        // 发送注册请求到后端处理
        fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                // 注册成功，跳转到其他页面
                window.location.href = '/前端网页/登录页面.html';
            } else {
                // 注册失败，显示错误消息
                console.log('Registration failed:', response);
                alert('该邮箱已注册过，请重新尝试！');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('发生错误，请稍后重试');
        });
    });
});