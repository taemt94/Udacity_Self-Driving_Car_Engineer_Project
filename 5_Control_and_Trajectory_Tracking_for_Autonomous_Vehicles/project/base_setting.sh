cd /home/workspace/nd013-c6-control-starter/project
./install-ubuntu.sh

/usr/bin/python3 -m pip install --upgrade pip
pip3 install pandas
pip3 install matplotlib

cd pid_controller/
rm -rf rpclib
git clone https://github.com/rpclib/rpclib.git

cmake .
make
