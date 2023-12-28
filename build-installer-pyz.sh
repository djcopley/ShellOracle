python3 -m pip install -r installer/requirements.txt --target installer
python3 -m zipapp -m install:install -p "/usr/bin/env python3" installer
