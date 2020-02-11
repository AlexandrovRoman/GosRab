enter.onclick = function(event)
{
    post_request("", {username: login.value, password: password.value});
}

function post_request(action, params)
{
    const form = document.createElement('form');
    form.method = 'post';
    form.action = action;

    for (const key in params)
    {
        if (params.hasOwnProperty(key))
        {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.name = key;
            hiddenField.value = params[key];
            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}