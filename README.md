# REST API built with Django REST framework

For this app, we combine **Django** (a free, open source framework based on Python) with an **REST API** (representational state transfer API).

The combination takes places through the **Django REST framework** (DRF) toolkit.

Since Django utilizes a **Model-View-Template** (MVT) architectural pattern, the toolkit is able to use the **class-based views**.

The outcome is a fully functional **CRUD** Django REST API.

# Endpoints
Endpoints define the structure and usage for the GET, POST, PUT, and DELETE HTTP methods within an RESTful API.

This app uses two endpoints:
|Endpoint|GET|POST|PUT|DELETE|View|
|:--:|:--:|:--:|:--:|:--:|:--:|
|``todos/api``|1. List All: List all to-dos for requested user|2. Create: Add a new to-do|N/A|N/A|``TodoListApiView``|
|``todos/api/<int:todo_id>``|3. Retrieve: Get a to-do with given ``todo_id``|N/A|4. Update: Update a to-do with given ``todo_id``|5. Delete: Delete a to-do with given ``todo_id``|``TodoDetailApiView``|

These endpoints can simply be accessed via their specific urls e.g.:
`http://127.0.0.1:8000/todos/api/`

![List](list-api.jpg)

`http://127.0.0.1:8000/todos/api/2`

![List](detail-api.jpg)


However, this code also feaures the possibility to submit a new entry via a form submission.

The form is located here: `http://127.0.0.1:8000/`

The associated view is `contact` which renders a from for the `todo` model and checks if it is valid.

![Form](todo-form.jpg)

The `@login_required` decorators ensures that only a logged in user can access the form. The logged in user is then automatically associated with the user's submitted task.

# Model serializer
The conversion of an Model object into an API-usable format (e.g. JSON) is done via a serializer. The Django REST framework does this via the ModelSerializer class (see `serializers.py`).

# Using the Fetch Api with Django Rest Framework
For the purpose of demonstrating the usage of the fetch API in connection with our endpoints, I have integrated a JavaScript (`script.js`).

## Acquire csrf token
First we need to acquire our csrf token (as decribed in the [documentaion](https://docs.djangoproject.com/en/4.2/howto/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false)):
```
// Acquiring the csrf token
function getCookie(name) {
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
```
## Fetch data from api using JavaScript
Afterwards we fetch data from our api endpoint:
```
// Example of fetching data from our api
fetch("/todos/api/1/", {
    method: "get",
    headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
}).then(function(response) {
    return response.json();
}).then(function(data) {
    console.log("Data is ok", data); // log data to console
}).catch(function(ex) {
    console.log("parsing failed", ex); // log error to console
});
```

Since I have implemented the script in the `contact.html` header, we get the following log within our console if we visit `http://127.0.0.1:8000/`:

![Fetch Api](./fetch-api.jpg)

If we compare this to what we get with our api endpoint (`http://127.0.0.1:8000/todos/api/1/`) we see that they are identical:

![Detail Api](./api-detail-1.jpg)


# Source
The code is based on tutorials: 
- [How to create a REST API with Django REST framework](https://blog.logrocket.com/django-rest-framework-create-api/)
- [Django And Fetch API Form Submissions –Without Page Reloading](https://ridwanray.medium.com/django-and-fetch-api-form-submissions-without-page-reloading-dc5106598005)
- [Using the Fetch Api with Django Rest Framework](https://gist.github.com/marteinn/3785ff3c1a3745ae955c)