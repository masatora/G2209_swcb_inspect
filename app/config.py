from __init__ import web
from os.path import join

web.config.OAS = False

if web.config['APP_ENV'] == 'prod':
  project_path = join('/', 'app')
  web.config.update({
    'DEBUG': True,
    'WORKERS': 16,
    'CORS_ORIGINS': '*',
    'PROJECT_PATH': project_path,
    'STATIC_PATH': join(project_path, 'statics')
  })
elif web.config['APP_ENV'] == 'stage':
  project_path = join('D:\\', 'G2209_swcb_inspect')
  web.config.update({
    'DEBUG': True,
    'WORKERS': 1,
    'CORS_ORIGINS': '*',
    'PROJECT_PATH': project_path,
    'STATIC_PATH': join(project_path, 'app', 'statics')
  })
elif web.config['APP_ENV'] == 'beta':
  project_path = join('D:\\', 'ProgramFiles', 'project', 'G2209_swcb_inspect')
  web.config.update({
    'DEBUG': True,
    'WORKERS': 1,
    'CORS_ORIGINS': '*',
    'PROJECT_PATH': project_path,
    'STATIC_PATH': join(project_path, 'app', 'statics')
  })
else:
  project_path = join('C:\\', 'Users', 'masatora', 'git_repo', 'G2209_swcb_inspect')
  web.config.update({
    'DEBUG': True,
    'WORKERS': 1,
    'CORS_ORIGINS': '*',
    'PROJECT_PATH': project_path,
    'STATIC_PATH': join(project_path, 'app', 'statics')
  })
