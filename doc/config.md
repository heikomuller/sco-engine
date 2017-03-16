Configure RabbitMQ
==================


Setup user for SCO Worker process
---------------------------------

###Create SCO Worker user

sudo rabbitmqctl add_user {username} {password}

###Set permissions for SCO Worker user to read/write on SCO queue

sudo rabbitmqctl set_permissions -p / {username} "{queue}" ".*" ".*"

###Open RabbitMQ port

sudo ufw allow 5672


RabbitMQ Administrator
----------------------

Optional: Delete the default guest and create a new administrator

###Delete guest user

sudo rabbitmqctl delete_user guest

###Create new administrator

sudo rabbitmqctl add_user {administrator} ...
sudo rabbitmqctl set_user_tags {administrator} administrator
