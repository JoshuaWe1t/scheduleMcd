const txtBoxLogin = document.getElementById("login"),
    txtBoxPassword = document.getElementById('password'),
    btnSingIn = document.getElementById("btn-sign-in")
    // data = [
    //     {
    //         login: "test1234",
    //         password: 'test1234'
    //     },
    //     {
    //         login: "admin1234",
    //         password: "admin1234"
    //     }
    // ];
    data = {
        status: false,
        user_data: {
            code: "000000",
            password: F42ACBD5644,
            id_specialization: 0,
            id_department: 27000
        }
    }

let userName = '', userPswrd = '';

txtBoxLogin.addEventListener('change', e => {
    userName = e.target.value;
})

txtBoxPassword.addEventListener('change', e => {
    userPswrd = e.target.value;
})

btnSingIn.addEventListener('click', e => {
    user_data = {
        login: userName,
        password: userPswrd
    }
    for (let i = 0; i < data.length; i++) {
        console.log(data[i])
        if (userName === 'test1234' && userPswrd === 'test1234') {
            handleLoginSuccess(userName);
            redirectToEmployeePage();
            break;
        }
        else if (userName === 'admin1234' && userPswrd === 'admin1234') {
            handleLoginSuccess(userName);
            redirectToManagerPage();
            break;
        }
         else {
            console.log("Error: Invalid password or username");
        }
    }
    return user_data;
})

function redirectToEmployeePage() {
    window.location.href = "employee.html"; // Путь к целевой странице
}

function redirectToManagerPage() {
    window.location.href = "manager.html"; // Путь к целевой странице
}

function handleLoginSuccess(username) {
    localStorage.setItem('username', username);
}