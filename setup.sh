sudo apt update
sudo apt install -y openjdk-17-jdk
sudo apt install -y maven

sudo rm -rf /opt/spark
wget https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3-scala2.13.tgz   -P /tmp
sudo tar -xvzf /tmp/spark-3.5.1-bin-hadoop3-scala2.13.tgz -C /opt
sudo mv /opt/spark-3.5.1-bin-hadoop3-scala2.13 /opt/spark
rm /tmp/spark-3.5.1-bin-hadoop3-scala2.13.tgz  

echo "run 'source /etc/profile' for the changes to take effect."

# Add to bashrc and update
# export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# export SPARK_HOME=/opt/spark
# export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin