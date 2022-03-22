#!/bin/bash

echo-blue () {
    echo -e "\e[34m\e[1m$1\e[0m"
}

echo-red () {
    echo -e "\e[31m\e[1m$1\e[0m"
}

echo-blue "#########################"
echo-blue "## Installing managers ##"
echo-blue "#########################"

# polybar
sudo apt install rofi compton compton-conf nitrogen

echo-blue "#####################"
echo-blue "## Setting up rofi ##"
echo-blue "#####################"

git clone https://github.com/emanuelep57/Qminimize.git ~/.local/bin/qmm
cp ~/.local/bin/qmm/Qminimize ~/.local/bin/Qminimize
rm -rf ~/.local/bin/qmm
chmod +x ~/.local/bin/Qminimize

cp -r rofi ~/.config/

echo-blue "#############################"
echo-blue "## Setting up dependencies ##"
echo-blue "#############################"

sudo apt install xserver-xorg libwlroots-dev libpangocairo-1.0-0 \
python3-dbus python3-psutil \
python3-ewmh python3-fuzzywuzzy

# no packages
pip3 install uptime

# needs separate coz of bindings
pip3 install xcffib
pip3 install --no-cache-dir cairocffi

echo-blue "######################"
echo-blue "## Installing qtile ##"
echo-blue "######################"

pip3 install qtile

echo-blue "######################"
echo-blue "## Setting up qtile ##"
echo-blue "######################"

sudo cp qtile.desktop /usr/share/xsessions/qtile.desktop

chmod +x qtile/autostart.sh
cp -r qtile ~/.config/
