class GitHubAPIError(Exception):
    """Base GitHub API error."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class GitHubAPIRequestError(GitHubAPIError):
    """GitHub API request error."""



class GitHubAPIStatusError(GitHubAPIError):
    """GitHub API status error."""


