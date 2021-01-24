host="samireland.com"

docker-compose build

docker-compose push

ssh $host "mkdir samireland"

scp production.yml $host:~/samireland/docker-compose.yml
scp secrets.env $host:~/samireland/

ssh $host "cd samireland && docker-compose pull"
ssh $host "cd samireland && docker-compose up --remove-orphans -d"
ssh $host "cd samireland && docker network connect bridge samireland_nginx_1 2>/dev/null"
ssh $host "cd samireland && docker-compose exec django python manage.py migrate"

ssh $host "rm -r samireland"