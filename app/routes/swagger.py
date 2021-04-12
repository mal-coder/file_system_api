from flask_swagger_ui import get_swaggerui_blueprint

url = '/swagger'
api_url = '/static/swagger.yaml'
bp = get_swaggerui_blueprint(
    url,
    api_url,
    config={
        'app_name': "Seznam API"
    }
)
