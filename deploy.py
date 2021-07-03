import os

# print message
print("\033[0;32mBuilding project for pypi...\033[0m\n")

# build package
os.system("python setup.py sdist")
# upload package
os.system("twine upload dist/*")

print("\033[0;32mDeployment finished...\033[0m\n")