#!/bin/bash

echo "Cleaning output directories..."
rm -rf /home/nbl2005/DS200.Q21.1.LAB/DS200.Q21.1.Lab01/output/*
rm -rf /home/nbl2005/DS200.Q21.1.LAB/DS200.Q21.1.Lab01/BaiTap/*/target
find /home/nbl2005/DS200.Q21.1.LAB/DS200.Q21.1.Lab01/BaiTap -name "*.class" -delete
echo "Clean completed!"
