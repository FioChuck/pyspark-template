sudo apt update
sudo apt install -y openjdk-11-jdk
sudo apt install -y maven

# sudo rm -rf /opt/spark
# wget https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3-scala2.12.tgz   -P /tmp
# sudo tar -xvzf /tmp/spark-3.5.1-bin-hadoop3-scala2.12.tgz -C /opt
# sudo mv /opt/spark-3.5.1-bin-hadoop3-scala2.12 /opt/spark
# rm /tmp/spark-3.5.1-bin-hadoop3-scala2.12.tgz  sudo rm -rf /opt/spark
wget https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz   -P /tmp
sudo tar -xvzf /tmp/spark-3.5.1-bin-hadoop3.tgz -C /opt
sudo mv /opt/spark-3.5.1-bin-hadoop3 /opt/spark
rm /tmp/spark-3.5.1-bin-hadoop3.tgz  

