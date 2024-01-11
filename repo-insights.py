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
            if not suffix:
                suffix = '<no suffix>'
            files.append((file_content.name, suffix, line_count))
    return files


def suffix_based_stats(file_tuple_list):
    df = pd.DataFrame(data=file_tuple_list, columns=['name', 'suffix', 'line_count'])
    stats = df.groupby(['suffix']).agg(
        number_of_files=pd.NamedAgg(column='line_count', aggfunc='count'),
        total_line_count=pd.NamedAgg(column='line_count', aggfunc='sum')
    ).sort_values('number_of_files', ascending=False)
    print("Suffix Based Stats\n==================")
    print(stats)
    print()


def docker_related_files(file_tuple_list):
    docker_related = [x[0] for x in file_tuple_list if 'docker' in str.casefold(x[0])]
    print("Docker Related Files\n====================")
    print(len(docker_related), 'Docker related files found:', str(docker_related)[1:-1])
    print()


FILE_TO_MANAGER_MAP = {
    'package.json': 'NPM',
    'yarn.lock': 'Yarn',
    'requirements.txt': 'Pip',
    'Pipfile': 'Pipenv',
    'Gemfile': 'RubyGems',
    'composer.json': 'Composer',
    'pom.xml': 'Maven',
    'build.gradle': 'Gradle',
    '.csproj': 'NuGet',
    'Brewfile': 'Homebrew',
    'go.mod': 'Go Modules',
    'bower.json': 'Bower',
    'project.clj': 'Leiningen',
    'environment.yml': 'Conda',
    'Cargo.toml': 'Cargo',
    'Package.swift': 'Swift Package Manager',
}


def package_managers(file_tuple_list):
    manager_indicator_files = [x[0] for x in file_tuple_list if x[0] in FILE_TO_MANAGER_MAP]
    manager_indicator_files = list(set(manager_indicator_files))
    print("Package Managers\n================")
    print(len(manager_indicator_files), 'package managers found:', str([FILE_TO_MANAGER_MAP[x] for x in manager_indicator_files])[1:-1])
    print()


def generate_insights(repo_path, token):
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_path)

    # Fetch repo data from Github
    file_tuple_list = get_all_file_names(repo)
    pprint.pprint(file_tuple_list)

    # source code stats by file suffix
    suffix_based_stats(file_tuple_list)

    # Docker related files
    docker_related_files(file_tuple_list)

    # Package managers
    package_managers(file_tuple_list)

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
