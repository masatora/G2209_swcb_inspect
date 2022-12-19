from __init__ import web

if __name__ == '__main__':
  web.run(host=web.config['HOST'], port=10091, debug=web.config['DEBUG'], auto_reload=web.config['DEBUG'], access_log=False, workers=web.config['WORKERS'])
