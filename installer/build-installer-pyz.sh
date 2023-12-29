python -m pip install -r requirements.txt --target installer
python -m zipapp -m install:install -p "/usr/bin/env python3" installer
