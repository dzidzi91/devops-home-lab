Vagrant.configure("2") do |config|
  require 'rbconfig'
  host_cpu = RbConfig::CONFIG['host_cpu']

default_box = "ubuntu/jammy64"
arm_box = ENV.fetch('VAGRANT_ARM_BOX', "bento/ubuntu-22.04")

  if host_cpu == 'arm64'
    config.vm.box = arm_box
    config.vm.box_architecture = "arm64"
  else
    config.vm.box = default_box
  end

  config.vm.hostname = "devops-control"
  config.vm.network "private_network", ip: "192.168.56.10"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "devops-control"
    vb.memory = 4096
    vb.cpus = 2
  end
  config.vm.provision "shell", path: "./scripts/bootstrap.sh"
end
