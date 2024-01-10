from github import Github
import pprint

# Authentication is defined via github.Auth
from github import Auth


def x(file_content):
    if file_content.type == "dir":
        print("DIR", file_content.path)
        contents = repo.get_contents(file_content.path)
        for fc in contents:
            x(fc)
    else:
        print("\t", file_content.path)



# using an access token
auth = Auth.Token("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")

# First create a Github instance:

# Public Web Github
g = Github(auth=auth)
print(55,g)


# Then play with your Github objects:
u= g.get_user()
print(99, u)
for repo in g.get_user().get_repos():
     print(repo.name)

repo = g.get_repo("mosheco/appster2")
print(repo.name)

for i in range(1000000):
    print (i)
    contents = repo.get_contents("")
    print(contents)

for file_content in   contents:
    x(file_content)


# To close connections after use
g.close()

