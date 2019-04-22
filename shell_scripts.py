MONGO_SCRIPT = '''
apt-get install dirmngr -y

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

RABBIT_SCRIPT = '''
apt-get install dirmngr -y

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