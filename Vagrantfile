Vagrant.configure("2") do |config|

    config.vm.define "demo" do |demo|
        demo.vm.box = "ubuntu/bionic64"
        demo.vm.hostname = "demo"
        demo.vm.network "private_network", ip:"20.0.0.20"
        demo.vm.provision "shell", inline:"sed -i '$ a 20.0.0.20 database' /etc/hosts"
        demo.vm.provision "shell", inline:<<-SCRIPT
            sudo apt-get update
            sudo apt-get install -y redis-server python3-pip python3-venv git
            git clone https://github.com/cs334s21/capstone2021
            cd capstone2021
            sudo python3 -m venv .venv
            source .venv/bin/activate
            sudo pip3 install -e .

            # Copy services into system folder and make shell scripts executable
            sudo cp scripts/*.service /etc/systemd/system
            sudo chmod +x scripts/*.sh
        SCRIPT
        demo.vm.provision "shell", run: "always", inline:<<-SCRIPT
            # Start services that run the demo
            sudo systemctl start redis
            sudo systemctl start workgen
            sudo systemctl start workserver
            sudo systemctl start client
            sudo systemctl start dashboard
        SCRIPT
    end
end
