# TODO: This should be a separate recipe
# TODO: "main/vagrant" is bad. Recipes should be based on what things do
# not where things are

service node[:ssh][:service] do
    action [:enable, :start]
end

ssh_users = node[:users].select { |u| u[:ssh] }
ssh_users_with_keys = ssh_users.select { |u| u[:ssh_keys] }
ssh_users.each do |user|
    user_account user[:name] do
        ssh_keys user[:ssh_keys]
        manage_home true
        home "/home/#{user[:name]}"
        action :create
        shell '/bin/bash'
    end
end
group node[:ssh][:group] do
    members ssh_users.collect { |u| u[:name] }
    action :create
end

admin_users = node[:users].select { |u| u[:admin] }
group node[:admin_group] do
    members admin_users.collect { |u| u[:name] }
    action :create
end

sudo_users = node[:users].select { |u| u[:sudo] }
group 'sudo' do
    members sudo_users.collect { |u| u[:name] }
    action :create
end

if node[:custom_sudoers] then
    template "/etc/sudoers.d/#{node[:custom_sudoers]}" do
        source 'sudoers.erb'
        mode '0440'
    end
end


template '/etc/ssh/sshd_config' do
    source 'sshd_config.erb'
    mode '0644'
    notifies :restart, "service[#{node[:ssh][:service]}]"
end
