import argparse
import base64
from github import Github, Auth
import pandas as pd
import pathlib
import pprint


def get_all_file_names(repo):
    files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            line_count = base64.b64decode(file_content.content).decode().count('\n')
            suffix = pathlib.Path(file_content.name).suffix
            files.append((file_content.name, suffix, line_count))
    return files


def suffix_based_stats(file_tuple_list):
    df = pd.DataFrame(data=file_tuple_list, columns=['name', 'suffix', 'line_count'])
    stats = df.groupby(['suffix'])['line_count'].agg(['sum', 'count']).sort_values('count', ascending=False)
    print(stats)


def generate_insights(repo_path, token):
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_path)

    file_tuple_list = get_all_file_names(repo)
    pprint.pprint(file_tuple_list)

    suffix_based_stats(file_tuple_list)

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
