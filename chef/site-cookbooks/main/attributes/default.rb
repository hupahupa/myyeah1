default[:web][:app_name] = 'web'
default[:web][:app_user] = 'web'
default[:web][:db][:database] = 'web'
default[:web][:db][:host] = 'localhost'
default[:web][:db][:user] = 'web'
default[:web][:port] = 8129
default[:web][:stat_port] = 24225
default[:web][:secret_key] = 'dHKEf1IXUVQzs9ubg6pHULHaAOUaL0pod'
default[:web][:python][:virtualenv] = '/home/web/.virtualenvs/web'
default[:web][:server_aliases] = []

default[:nvm][:reference] = 'v0.5.1'
set[:nodejs][:version] = '0.10.18'
set[:nodejs][:npm][:version] = '1.3.8'

#environment: local or dev or prod
default[:web][:env] = 'dev'

#db log debug
default[:web][:db][:debug] = false

#emails
default[:web][:emails][:admin] = 'duyleminh1402+admin@gmail.com'
default[:web][:emails][:mandrill][:api_key] = 'mlMXJDqixFlKwsvbTdWM7g'

#email to send error
default[:web][:emails][:errors] = [
]
default[:web][:emails][:debug] = false

default[:web][:debug] = true

default[:nginx][:client_max_body_size] = '3M'
default[:web][:blocked_keywords] = [
    "/phpMyAdmin",
    "/mysqladmin",
    "/muieblackcat",
    "/manager/html",
    "/test",
    "/proxy.txt",
    ".php",
]
