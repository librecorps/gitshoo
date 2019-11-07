from github import Github
from github.GithubException import GithubException
from getpass import getpass
import fire


def get_gh_client(auth_type):
    if auth_type == 'token':
        token = getpass(prompt='Github Access Token: ')
        gh = Github(token)
    elif auth_type == 'user':
        username = input("Username: ")
        password = getpass()
        gh = Github(username, password)
    return gh


class Gitshoo(object):
    """
    Migrate all issue labels from one repository to another
    :param from_repo: Repository you are migrating from in the format of `username/repo`
    :param to_repo: Repository you are migrating to in the format of `username/repo`
    :param auth: How to auth to Github. Default is `token`. Also available is `username`
    """


    def __init__(self, from_repo, to_repo, auth='token'):
        gh = get_gh_client(auth)
        fr = gh.get_repo(from_repo)
        to = gh.get_repo(to_repo)

        labels = fr.get_labels()
        for label in labels:
            print(f'Creating label {label.name}')

            try:
                if label.description is None:
                    to.create_label(label.name, label.color)
                else:
                    to.create_label(label.name, label.color, label.description)
            except GithubException as e:
                if e.status == 422:  # Label already exists
                    pass
                else:
                    raise(e)


if __name__ == '__main__':
    fire.Fire(Gitshoo)
