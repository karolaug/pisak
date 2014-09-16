#!/bin/bash

# Downloads and install Kelson Sans font

FONT_URL="http://fontfabric.com/downfont/kelson.zip"

# download
echo "Downloading..."
wget $FONT_URL -O /tmp/kelson.zip

# create font dir
echo "Installing..."
mkdir -p $HOME/.fonts

# install fonts
cd $HOME/.fonts
unzip -n /tmp/kelson.zip

# update font cache
echo "Updating font cache..."
fc-cache

# cleanup
echo "Cleaning up..."
rm /tmp/kelson.zip

echo "Done!"

