MONGO_SCRIPT = '''
apt-get install dirmngr wget -y

apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5

echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/3.6 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list

apt-get update

apt-get install mongodb-org -y

echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
'''

MONGO_REPLICA_SET_SCRIPT = '''
apt-get install dirmngr wget -y

apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5

echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/3.6 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list

apt-get update

apt-get install mongodb-org -y

echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections

mkdir -p /data/mongodb/one /data/mongodb/two /data/mongodb/three
chmod 755 /data
chown -R mongodb:mongodb /data/mongodb
mkdir -p /var/log/mongodb/one /var/log/mongodb/two /var/log/mongodb/three
chown -R mongodb:mongodb /var/log/mongodb
sudo -u mongodb -g mongodb mongod --replSet rs0 --port 27017 --dbpath /data/mongodb/one --fork --logpath /var/log/mongodb/one/mongod.log
sudo -u mongodb -g mongodb mongod --replSet rs0 --port 27027 --dbpath /data/mongodb/two --fork --logpath /var/log/mongodb/two/mongod.log
sudo -u mongodb -g mongodb mongod --replSet rs0 --port 27037 --dbpath /data/mongodb/three --fork --logpath /var/log/mongodb/three/mongod.log
sleep 5

mongo --port 27017 <<EOF
    rs.initiate({_id: "rs0", members: [
        {_id: 0, host: "localhost:27017"},
        {_id: 1, host: "localhost:27027"},
        {_id: 2, host: "localhost:27037", arbiterOnly: true}
    ], settings: {electionTimeoutMillis: 2000}});
EOF
'''

RABBIT_SCRIPT = '''
apt-get install dirmngr wget -y

apt-key adv --keyserver "hkps.pool.sks-keyservers.net" --recv-keys "0x6B73A36E6026DFCA"

wget -O - "https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc" | apt-key add -

apt-get install apt-transport-https

printf "deb https://dl.bintray.com/rabbitmq-erlang/debian stretch erlang" > /etc/apt/sources.list.d/bintray.rabbitmq.list
printf "deb https://dl.bintray.com/rabbitmq/debian stretch main"         >> /etc/apt/sources.list.d/bintray.rabbitmq.list

apt-get update -y

apt-get install erlang -y

printf "Package: erlang*\nPin: release o=Bintray\nPin-Priority: 1000" > /etc/apt/preferences.d/erlang

apt-get update

apt-get install rabbitmq-server -y
'''