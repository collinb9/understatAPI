if [ ! -f "/usr/local/bin/geckodriver" ]; then
    wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
    tar -xvzf geckodriver*
    chmod +x geckodriver
    sudo mv geckodriver /usr/local/bin/
fi
pip install -r requirements.txt -r test_requirements.txt
pip install -r docs/requirements.txt

