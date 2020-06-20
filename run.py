from app import urls, app, config

urls.register_blueprints()
if app.debug:
    app.run(config.HOST, config.PORT)
