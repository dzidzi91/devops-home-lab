Vagrant.configure("2") do |config|
  require "rbconfig"

  host_cpu = RbConfig::CONFIG["host_cpu"]

  default_box = "ubuntu/jammy64"
  arm_box     = ENV.fetch("VAGRANT_ARM_BOX", "bento/ubuntu-22.04")

  if host_cpu == "arm64"
    config.vm.box = arm_box
    config.vm.box_architecture = "arm64"
  else
    config.vm.box = default_box
  end

  #################################
  # DEVOPS CONTROL
  #################################
  config.vm.define "management" do |dc|
    dc.vm.hostname = "devops-control"
    dc.vm.network "private_network", ip: "192.168.56.10"

    dc.vm.provider "virtualbox" do |vb|
      vb.name = "devops-control"
      vb.memory = 4096
      vb.cpus = 2
    end
  end

  #################################
  # CONTROL PLANE
  #################################
  config.vm.define "control-plane" do |cp|
    cp.vm.hostname = "control-plane"
    cp.vm.network "private_network", ip: "192.168.56.11"

    cp.vm.provider "virtualbox" do |vb|
      vb.name = "control-plane"
      vb.memory = 2048
      vb.cpus = 2
    end
  end

  #################################
  # WORKER 1
  #################################
  config.vm.define "worker-1" do |worker1|
    worker1.vm.hostname = "worker-1"
    worker1.vm.network "private_network", ip: "192.168.56.12"

    worker1.vm.provider "virtualbox" do |vb|
      vb.name = "worker-1"
      vb.memory = 2048
      vb.cpus = 1
    end
  end

  #################################
  # WORKER 2
  #################################
  config.vm.define "worker-2" do |worker2|
    worker2.vm.hostname = "worker-2"
    worker2.vm.network "private_network", ip: "192.168.56.13"

    worker2.vm.provider "virtualbox" do |vb|
      vb.name = "worker-2"
      vb.memory = 2048
      vb.cpus = 1
    end
  end
end