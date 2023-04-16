set -eo pipefail

if [ $CODESPACES ]; then
    PATH_TO_CODE="${OLDPWD}"
else
    PATH_TO_CODE="/workspaces/app/"
fi

export PIPENV_VERBOSITY=-1

echo -e "\n###############################################################"
echo -e "Setting up Python Environment \n"

cd ${PATH_TO_CODE}

pipenv install --dev

echo -e "\n###############################################################"
echo -e  "Run Web Server ... \n"

cd ${PATH_TO_CODE}/build/

pipenv run dev