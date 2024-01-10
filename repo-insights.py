import argparse
from github import Github, Auth
import pprint

def x(file_content, repo):
    if file_content.type == "dir":
        print("DIR", file_content.path)
        contents = repo.get_contents(file_content.path)
        for fc in contents:
            x(fc, repo)
    else:
        print("\t", file_content.path)


def generate_insights(repo_path, token):
    auth = Auth.Token(token)
    g = Github(auth=auth)
    print(55,g, repo_path, token)

    repo = g.get_repo(repo_path)
    print(repo.name)

    contents = repo.get_contents("")
    print(contents)

    for file_content in   contents:
        x(file_content, repo)

    g.close()


def get_parser():
    """
    Parse the command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo',
                        help="full path of repo (<user>/<name>)",
                        dest='repo',
                        required=True)

    parser.add_argument('--token',
                        help="an access token provided by Github",
                        default="token",
                        required=True)

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    generate_insights(args.repo, args.token)

