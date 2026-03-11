set -e
ssh root@104.248.96.25 'cd /home/administrator/simulate_ecom && git pull --recurse-submodules'
ssh root@104.248.96.25 'cd /home/administrator/simulate_ecom && docker compose -f docker-compose.prod.yml up -d --build'
ssh root@104.248.96.25 'cp /home/administrator/simulate_ecom/infrastructure/nginx.conf /etc/nginx/sites-enabled/simulate_ecom.conf'
ssh root@104.248.96.25 'sudo nginx -s reload'



cp /home/administrator/simulate_ecom/infrastructure/nginx.conf /etc/nginx/sites-enabled/simulate_ecom.conf