import os
import re
import shutil

def create_env_folder():
    parent_dir = os.path.realpath(os.path.expanduser("."))
    dir_name = "env_files/" # Change name back to original
    env_path = os.path.join(parent_dir, dir_name)
    if(os.path.exists(env_path)):
        shutil.rmtree(env_path)
    os.mkdir(env_path)

    return env_path

def get_total_client_number():
    matches = []
    with open('docker-compose.yml') as file:
        for line in file:
            match = re.findall("(client\d.env|client\d\d.env)", line)
            if len(match) == 1:
                matches += match
    return matches

def write_files(api_key, env_path, total_clients):
    # Write client files
    for i in range(1, len(total_clients) + 1):
          with open("{}client{}.env".format(env_path, i), 'w') as file:
            file.write("WORK_SERVER_HOSTNAME=work_server" + "\n")
            file.write("WORK_SERVER_PORT=8080" + "\n")
            file.write("API_KEY={}".format(api_key) + "\n")
            file.write("ID={}".format(i) + "\n")
            file.write("PYTHONUNBUFFERED=TRUE")

    # Write work generator file
    with open("{}work_gen.env".format(env_path), 'w') as file:
        file.write("API_KEY={}".format(api_key) + "\n")
        file.write("PYTHONUNBUFFERED=TRUE")

    # Write dashboard file
    with open("{}dashboard.env".format(env_path), 'w') as file:
        file.write("MONGO_HOSTNAME=mongo" + "\n")
        file.write("REDIS_HOSTNAME=redis" + "\n")
        file.write("PYTHONUNBUFFERED=TRUE")
    
    # Create data folder 
    parent_dir = os.path.realpath(os.path.expanduser("~"))
    dir_name = "data/"
    data_path = os.path.join(parent_dir, dir_name)

    if(not os.path.exists(data_path)):
        os.mkdir(data_path)


if __name__ == "__main__":

    # Get user input for API key
    api_key = input("Enter your API key from regulations.gov: ")

    env_path = create_env_folder() 
    total_clients = get_total_client_number()

    write_files(api_key, env_path, total_clients)

            

