# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = 'trusty64'

    config.vm.network :forwarded_port, guest: 80, host: 9600
    config.vm.network :forwarded_port, guest: 22, host: 9601, id: "ssh", auto_correct: true

    apt_cache = './apt-cache'
    FileUtils.mkpath "#{apt_cache}/partial"

    chef_cache = '/var/chef/cache'

    shared_folders = {
        apt_cache => '/var/cache/apt/archives',
        './.cache/chef' => chef_cache,
    }

    config.vm.provider :virtualbox do |vb|

        #vb.gui = true

        shared_folders.each do |source, destination|
            FileUtils.mkpath source
            config.vm.synced_folder source, destination
            vb.customize ['setextradata', :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/#{destination}", '1']
        end

        vb.customize ['setextradata', :id, 'VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root', '1']
    end

    config.vm.provision :chef_solo do |chef|

        chef.provisioning_path = chef_cache

        chef.cookbooks_path = [
            'chef/chef-cookbooks',
            'chef/site-cookbooks',
        ]

        chef.json = {
            :web => {
                :server_names => ['localhost'],
                :log_dir => '/vagrant/logs',
                :site_dir => '/vagrant',
                :db => {
                    :password => 'vagrant',
                },
                :app_user => 'vagrant',
                :email => {
                    :admin => 'admin@vagrant.local',
                    :sender => 'sender@vagrant.local',
                },
                :site_name => 'web',
                :env => 'local'
            },

            # Vagrant attributes
            :apache => {
                :user => 'vagrant',
            },
            :php => {
                :fpm => {
                    :user => 'vagrant',
                },
            },
            :nginx => {
                :sendfile => 'off',
                :version => '1.6.2',
            },
            :mysql => {
                :server_root_password => 'vagrant',
            },
            :users => [
                {
                    :name => "vagrant",
                    :ssh => true,
                    :sudo => true,
                    :admin => true,
                }
            ],
            :custom_sudoers => "web",
            :postgresql => {
                :client_auth => [
                    {
                        :type => 'local',
                        :database => 'all',
                        :user => 'all',
                        :auth_method => 'trust',
                    }
                ],
                :version => '9.4'
            }
        }

        chef.add_recipe 'vagrant'

        #chef.data_bags_path = '../my-recipes/data_bags'
    end
end
