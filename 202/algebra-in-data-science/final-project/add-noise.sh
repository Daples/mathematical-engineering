#!/bin/bash

inputs=$(find . -name "input.jpg")
for line in $inputs; do
    echo Adding noise to $line...
    directory=$(dirname $line)
    magick $line +noise Gaussian $directory/input-gaussian.jpg
    magick $line +noise Impulse $directory/input-impulse.jpg
done
echo Finished!
