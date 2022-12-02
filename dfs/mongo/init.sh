mongod --bind_ip_all
mongosh --eval "db.getSiblingDB('ziem').createUser({user:'zuser', pwd:'123456', roles:[{role:'readWrite', db:'ziem'}]})"
do
    sleep 1
done
mongod --bind_ip_all