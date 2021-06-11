let under_popup = document.getElementById('under-popup')
let login_popup = document.getElementById('popup-login')
let register_popup = document.getElementById('popup-register')


$('#header-login').on('click', function () {
    $('#under-popup').css('display', 'block')
    $('#popup-login').css('display', 'block')
    document.body.style.overflow = 'hidden';
});

$('#header-register').on('click', function () {
    $('#under-popup').css('display', 'block')
    $('#popup-register').css('display', 'block')
    document.body.style.overflow = 'hidden';
})

$('#under-popup').on('mousedown', function (event) {
    if (event.target === this) {
        $('#under-popup').css('display', 'none')
        document.body.style.overflow = 'auto'
        $('#popup-login').css('display', 'none')
        $('#popup-register').css('display', 'none')
    }
})

function getCookie(name) {
    // Принимает в параметр имя куки и возвращает её значение
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


// Нижу предоставлены ajax запросы для обмена данными с сервером


$.ajaxSetup({
    headers: {'X-CSRFToken': csrftoken}
});

let auth = function (event) {
    event.preventDefault()
    let auth_login = $("#popup-login-form-login").val()
    let auth_password = $("#popup-login-form-password").val()
    $.post('/auth/login/', {task: 'send', login: auth_login, password: auth_password}, function (data) {
        if (data.auth == 'ok') {
            location.reload()
        } else if (data.auth == 'bad_auth') {
            $("#popup-login-form-password").val('')
            alert('Неверный логин или пароль')
        }
    })
}
$('#header-login').one('click', function () {
    $.post('/auth/login/', {task: 'get_form'}, function (data) {
        $('#popup-login').html(data.html)
        $('#popup-login-form-send').on('click', auth)
    })

});

let reg = function (event) {
    event.preventDefault()
    let username = $("#popup-register-form-login").val()
    let pass1 = $("#popup-register-form-password1").val()
    let pass2 = $("#popup-register-form-password2").val()
    $.post('/auth/register/', {task: 'send', username: username, password1: pass1, password2: pass2}, function (data) {
        if (data.valid) {
            location.reload()
        } else {
            if (data.password2) {
                data.password2.forEach(function (i) {
                    if (i['code'] == 'password_mismatch') {
                        alert('Пароли не совпадают')
                    }
                    if (i['code'] == 'len_password_error') {
                        alert('Длинна пароля не менее 6 символов')
                    }
                })
            }
            if (data.username) {
                data.username.forEach(function (i) {
                    if (i['code'] == 'unique') {
                        alert('Такое имя пользователя уже существует')
                    }
                    if (i['code'] == 'len_login_error') {
                        alert('Логин от 4 до 20 символов')
                    }
                    if (i['code'] == 'invalid') {
                        alert('Неверный логин. Логин может содержать тольк буквы, цифры и символы @/./+/-/_')
                    }
                })
            }
        }
    })
}
$('#header-register').one('click', function () {
    $.post('/auth/register/', {task: 'get_form'}, function (data) {
        $('#popup-register').html(data.html)
        $('#popup-register-form-send').on('click', reg)
    })
})

$('.reply-comment-btn').on('click', function (e) {
        let $field = $('#new-comment-field')
        $(window).scrollTop($field.offset().top)
        $field.val(e.currentTarget.parentElement.firstElementChild.firstElementChild.innerHTML + ', ')
        $field.focus()
        $field[0].setSelectionRange($field.val().length, $field.val().length)
    }
)
jQuery.datetimepicker.setLocale( 'ru' )
$('#id_start_time').datetimepicker({
    format: 'Y-m-d H:i:00',
    step: 5,
    minDate: 0,
    dayOfWeekStart: 1,
})
