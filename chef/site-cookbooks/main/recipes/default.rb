
include_recipe 'apt'
include_recipe 'nginx'
include_recipe 'git'
include_recipe 'python'
include_recipe 'nodejs'
include_recipe "postgresql::client"
include_recipe "main::database"

web = node[:web]
app_user = web[:app_user]
db = web[:db]
python_env = web[:python][:virtualenv]
site_dir = web[:site_dir]
site_name = web[:site_name]
script_dir = "#{site_dir}/scripts"

%w{
    libjpeg-dev
    zlib1g-dev
    libpng12-dev
    libpq-dev
    libffi-dev
}.each do |pkg|
    package pkg do
        action :install
    end
end


user app_user do
    home "/home/#{app_user}"
    shell '/bin/bash'
    supports :manage_home => true
    action :create
end


[web[:log_dir], script_dir].each do |dir|
    directory dir do
        owner app_user
        action :create
        recursive true
    end
end

dirs = [
    "web/static/uploads",
]

dirs.each do |component|
    the_dir = "#{site_dir}/#{component}"
    bash 'setup permissions' do
        code <<-EOH
            mkdir -p #{the_dir}
            chown -R #{app_user} #{the_dir}
            chgrp -R www-data #{the_dir}
            chmod -R g+rw #{the_dir}
            find #{the_dir} -type d | xargs chmod g+x
        EOH
    end
end

# Install schemup dependencies
bash 'install schemup dependencies' do
    code <<-EOH
        . #{python_env}/bin/activate
        pip install -r #{site_dir}/schema/requirements.txt
    EOH
end

template "#{site_dir}/web_uwsgi.ini" do
    source 'web_uwsgi.ini.erb'
    owner app_user
end

template "#{site_dir}/run.py" do
    source 'run.py.erb'
    owner app_user
end

template "#{site_dir}/config/main.py" do
    source 'main.py.erb'
    owner app_user
end

template "#{script_dir}/set_env.sh" do
    source 'set_env.sh.erb'
    mode '755'
end

#start - stop - restart uwsgi service
template "#{script_dir}/start.sh" do
    source 'start.sh.erb'
    mode '755'
end

template "#{script_dir}/stop.sh" do
    source 'stop.sh.erb'
    mode '755'
end

template "#{script_dir}/restart.sh" do
    source 'restart.sh.erb'
    mode '755'
end

template "#{script_dir}/web.sh" do
    source 'web.sh.erb'
    mode '755'
end

template "/etc/init/#{site_name}.conf" do
    source 'upstart_web.erb'
    mode '644'
end

# script to excute i18n in Flask
template "#{script_dir}/tr_compile.sh" do
    source 'tr_compile.sh.erb'
    mode '755'
end

template "#{script_dir}/tr_update.sh" do
    source 'tr_update.sh.erb'
    mode '755'
end

template "#{script_dir}/tr_ini.sh" do
    source 'tr_ini.sh.erb'
    mode '755'
end

#deploy script
template "#{script_dir}/deploy.sh" do
    source 'deploy.sh.erb'
    mode '755'
end

#show stat script
template "#{script_dir}/monitor.sh" do
    source 'monitor.sh.erb'
    mode '755'
end

#db config
template "#{site_dir}/config/db.json" do
    source 'db.json.erb'
    mode '644'
end

directory python_env do
    action :create
    recursive true
end

python_virtualenv python_env do
    action :create
end

# Installing from requirements.txt
bash 'install python dependencies' do
    code <<-EOH
        . #{python_env}/bin/activate
        pip install -r #{site_dir}/requirements.txt
    EOH
end

service site_name do
    provider Chef::Provider::Service::Upstart
    action [:enable, :start]
end

# Nginx
template "/etc/nginx/sites-available/#{site_name}" do
    source 'nginx_web.erb'
    mode '644'
    notifies :reload, 'service[nginx]'
end

nginx_site site_name do
    action :enable
end

nginx_site 'default' do
    enable false
end

template "/etc/logrotate.d/yeah1.duyleminh.com" do
    source 'logrotate.erb'
    mode '644'
end
