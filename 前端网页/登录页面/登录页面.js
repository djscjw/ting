document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单默认提交行为

        // 获取表单中的邮箱、密码、是否记住密码和是否开发者登录
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;
        const developer = document.getElementById('developer').checked;

        // 构建发送到后端的数据对象
        const formData = {
            email: email,
            password: password,
            remember: remember,
            developer: developer
        };

        // 构建发送到后端的URL
        const url = developer ? 'http://localhost:5000/login-developer' : 'http://localhost:5000/login';

        // 发送表单数据到后端处理
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                // 根据开发者登录选项跳转到不同页面
                if (developer) {
                    // 开发者登录成功，跳转到用户反馈页面
                    window.open ('http://localhost:52330/%E5%89%8D%E7%AB%AF%E7%BD%91%E9%A1%B5/%E5%85%B6%E4%BB%96html,css,js%E4%BB%A3%E7%A0%81/%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF.html');
                } else {
                    // 普通用户登录成功，跳转到首页页面
                    window.open ('http://localhost:52330/%E5%89%8D%E7%AB%AF%E7%BD%91%E9%A1%B5/%E5%85%B6%E4%BB%96html,css,js%E4%BB%A3%E7%A0%81/%E9%A6%96%E9%A1%B5%E9%A1%B5%E9%9D%A2.html');
                }
            } else {
                // 登录失败，显示错误消息
                console.log('Login failed:', response);
                alert('登录失败，请检查邮箱和密码');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('发生错误，请稍后重试');
        });
    });
});