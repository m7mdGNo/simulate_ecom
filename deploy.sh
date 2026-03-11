set -e
ssh root@104.248.96.25 'cd /home/administrator/farm_ecommerce && git pull --recurse-submodules'
ssh root@104.248.96.25 'cd /home/administrator/farm_ecommerce && docker compose -f docker-compose.prod.yml up -d --build'
ssh root@104.248.96.25 'cp /home/administrator/farm_ecommerce/infrastructure/nginx.conf /etc/nginx/sites-enabled/farm_ecommerce.conf'
ssh root@104.248.96.25 'sudo nginx -s reload'