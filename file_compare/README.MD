A. python framework to compare the common files between 2 local or S3 folders

File formats supported
* csv (v1.0)
* xlsx (v1.1) - In progress



Additional features:
-- Detailed output with error records (Parameterized)
-- logging

Packages:
--------
-- to download the packages from machine which has internet
mkdir dependencies
pip download -r libraries.txt -d "./dependencies"
tar cvfz dependencies.tar.gz dependencies

And, once you transfer the dependencies.tar.gz to the machine which does not have internet you would do:
----------------------------
tar zxvf dependencies.tar.gz
cd dependencies
pip install * -f ./ --no-index

-----------------------------

code usage:
-----------
python3 -m venv autovenv
source autovenv/bin/activate
pip install -r libraries.txt




Usage:~/file_comp>pytest test_compare.py -s
