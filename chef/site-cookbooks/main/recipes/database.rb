site = node[:web]
db = site[:db]
site_dir = site[:site_dir]

include_recipe 'postgresql::server'

postgresql_user db[:user] do
  superuser true
  createdb true
  login true
  replication false
  password db[:password]
end

postgresql_database db[:database] do
  owner db[:user]
  encoding "utf8"
  template "template0"
  locale "en_US.UTF8"
end
