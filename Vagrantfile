Vagrant.configure("2") do |config|

    config.vm.define "workserver" do |workserver|
        workserver.vm.box = "ubuntu/trusty64"
        workserver.vm.hostname = "workserver"
        workserver.vm.network "private_network", ip:"20.0.1.100"

        workserver.vm.provision "shell", inline:<<-SCRIPT
            apt-get update && apt-get install -y python3-pip git
            git clone https://github.com/cs334s21/capstone2021
        SCRIPT
    end

    config.vm.define "client" do |client|
        client.vm.box = "ubuntu/trusty64"
        client.vm.hostname = "client"
        client.vm.network "private_network", ip:"20.0.1.200"
        # Add "workserver" to /etc/hosts, which allows the client
        # to connect to the name workserver by name
        client.vm.provision "shell", inline:"sed -i '$ a 20.0.1.100 workserver' /etc/hosts"

        client.vm.provision "shell", inline:<<-SCRIPT
            apt-get update && apt-get install -y python3-pip git
            git clone https://github.com/cs334s21/capstone2021
        SCRIPT
    end
end
