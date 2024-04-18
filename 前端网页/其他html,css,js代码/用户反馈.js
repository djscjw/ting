document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // 获取表单中的数据
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        // 构建包含表单数据的对象
        const formData = {
            name: name,
            email: email,
            message: message
        };

        // 发送表单数据到后端处理
        fetch('http://localhost:5000/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData) // 将对象转换为JSON格式
        })
        .then(response => {
            if (response.ok) {
                alert('反馈提交成功！');
                form.reset(); // 提交成功后重置表单
            } else {
                console.error('提交失败:', response);
                alert('提交失败，请稍后重试');
            }
        })
        .catch(error => {
            console.error('错误:', error);
            alert('发生错误，请稍后重试');
        });
    });
});