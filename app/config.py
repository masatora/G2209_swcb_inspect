from __init__ import web
from os.path import join

web.config.OAS = False
web.config.LOCAL_CERT_CREATOR = 'trustme'

if web.config['APP_ENV'] == 'prod':
  project_path = r'D:\\G2209_swcb_inspect'
  web.config.update({
    'DEBUG': False,
    'WORKERS': 16,
    'CORS_ORIGINS': '*',
    'PROJECT_PATH': project_path,
    'STATIC_PATH': project_path + '\\app\\statics',
    'PUBLIC_PATH': project_path + '\\vue'
  })
elif web.config['APP_ENV'] == 'stage':
  project_path = r'D:\\G2209_swcb_inspect'
  web.config.update({
    'DEBUG': True,
    'WORKERS': 1,
    'CORS_ORIGINS': '*',
    'PROJECT_PATH': project_path,
    'STATIC_PATH': project_path + '\\app\\statics',
    'PUBLIC_PATH': project_path + '\\vue'
  })
elif web.config['APP_ENV'] == 'beta':
  project_path = join('D:\\', 'ProgramFiles', 'project', 'G2209_swcb_inspect')
  web.config.update({
    'DEBUG': True,
    'WORKERS': 1,
    'CORS_ORIGINS': '*',
    'PROJECT_PATH': project_path,
    'STATIC_PATH': join(project_path, 'app', 'statics'),
    'PUBLIC_PATH': join(project_path, 'vue', 'public')
  })
else:
  project_path = r'C:\\Users\\masatora\\git_repo\\G2209_swcb_inspect'
  web.config.update({
    'DEBUG': True,
    'WORKERS': 1,
    'CORS_ORIGINS': '*',
    'PROJECT_PATH': project_path,
    'STATIC_PATH': project_path + '\\app\\statics',
    'PUBLIC_PATH': project_path + '\\vue\\public'
  })
