# TODO: This should be a separate recipe

default[:ssh][:enable_password] = false
default[:ssh][:hostkeys] = %w{
    /etc/ssh/ssh_host_rsa_key
    /etc/ssh/ssh_host_dsa_key
}
default[:ssh][:matches] = {}
default[:ssh][:ports] = [22]
default[:ssh][:group] = 'sshusers'

case node[:platform]
when 'redhat', 'centos', 'amazon'
    default[:ssh][:service] = 'sshd'
    default[:ssh][:sftp][:shell] = '/sbin/nologin'
    default[:ssh][:subsystems] = { 'sftp' => '/usr/libexec/openssh/sftp-server' }
when 'ubuntu'
    default[:ssh][:service] = 'ssh'
    default[:ssh][:sftp][:shell] = '/usr/sbin/nologin'
    default[:ssh][:subsystems] = { 'sftp' => '/usr/lib/openssh/sftp-server' }
    if node[:platform_version].to_f >= 12.04
        default[:ssh][:hostkeys] = %w{
            /etc/ssh/ssh_host_rsa_key
            /etc/ssh/ssh_host_dsa_key
            /etc/ssh/ssh_host_ecdsa_key
        }
    end
end

default[:admin_group] = 'admin'
default[:custom_sudoers] = nil
default[:sudo][:groups] = {}
default[:users] = []
