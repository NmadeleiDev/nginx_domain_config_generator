import argparse
import os


nginx_conf_template = 'server {{ \n\
    server_name		{} ; \n\
    location / {{ \n\
      proxy_pass      http://127.0.0.1:{}; \n\
    }} \n\
}}'


# parse args
parser = argparse.ArgumentParser()
parser.add_argument('--domain', help='Domain to create', required=True)
parser.add_argument('--container-port', help='Port of local container', required=True)
args = parser.parse_args()

domain = args.domain
cont_port = args.container_port

# create conf file
conf_files_dir = '/etc/nginx/sites-available'
conf_file = open(os.path.join(conf_files_dir, domain), "x")

conf_file.write(nginx_conf_template.format(domain, cont_port))

#create sites-enabled link
create_link_command = 'ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled/{}'
os.system(create_link_command.format(domain, domain))

# create ssl cret by sertbot
create_cert_command = 'certbot -n -d {} --nginx'
os.system(create_cert_command.format(domain))

print("Success")
