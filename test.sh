flake8 . --count --select=E9,F63,F7,F82 --show-source --statistic
# 
if output=$(coverage run test.py); then
    echo "Building HTML results"
    coverage html
else
    exit $?
fi

