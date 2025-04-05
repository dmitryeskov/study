from starlette.applications import Starlette
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from jinja2 import Environment, FileSystemLoader
import uvicorn

# Настройка Jinja2 для работы с шаблонами
templates = Environment(loader=FileSystemLoader("templates"))

# Главная страница
async def homepage(request):
    template = templates.get_template("index.html")
    content = template.render(title="Welcome", message="Hello from Starlette!")
    return HTMLResponse(content)

# Обработка формы (POST)
async def handle_form(request: Request):
    if request.method == 'POST':
        form_data = await request.form()
        name = form_data.get('name', 'Anonymous')
        user_id = form_data.get('user_id', '0')

        # Перенаправление на страницу профиля
        return RedirectResponse(url=f"/profile?name={name}&user_id={user_id}", status_code=302)

    # Если запрос не POST
    return HTMLResponse("Invalid request", status_code=400)

# Страница профиля
async def profile(request: Request):
    query_params = request.query_params
    name = query_params.get('name', 'Guest')
    user_id = query_params.get('user_id', 'Unknown')

    template = templates.get_template("profile.html")
    content = template.render(title="Profile", name=name, user_id=user_id)
    return HTMLResponse(content)

# Динамическая страница
async def dynamic_page(request: Request):
    template = templates.get_template("dynamic.html")
    items = [{"name": f"Item {i}", "value": i} for i in range(1, 11)]
    content = template.render(title="Dynamic Page", items=items)
    return HTMLResponse(content)

# Маршруты приложения
routes = [
    Route('/', homepage, methods=["GET"]),
    Route('/submit', handle_form, methods=["POST"]),
    Route('/profile', profile, methods=["GET"]),
    Route('/dynamic', dynamic_page, methods=["GET"]),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

# Приложение Starlette
app = Starlette(debug=True, routes=routes)

# Запуск сервера
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8007)
