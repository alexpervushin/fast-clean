from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Dict


class DataSourceType(StrEnum):
    GIT = "git"
    JIRA = "jira"
    ACTIVITY_WATCH = "activitywatch"
    GOOGLE_CALENDAR = "google_calendar"
    OUTLOOK_CALENDAR = "outlook_calendar"


@dataclass
class BaseDataSourceConfig:
    pass


@dataclass
class GitConfig(BaseDataSourceConfig):
    repository_path: str


@dataclass
class JiraConfig(BaseDataSourceConfig):
    server_url: str
    api_token: str


@dataclass
class ActivityWatchConfig(BaseDataSourceConfig):
    api_url: str


@dataclass
class CalendarConfig(BaseDataSourceConfig):
    credentials_json: Dict[str, Any] | None = None



DATA_SOURCE_CONFIG_MAP: Dict[DataSourceType, type[BaseDataSourceConfig]] = {
    DataSourceType.GIT: GitConfig,
    DataSourceType.JIRA: JiraConfig,
    DataSourceType.ACTIVITY_WATCH: ActivityWatchConfig,
    DataSourceType.GOOGLE_CALENDAR: CalendarConfig,
    DataSourceType.OUTLOOK_CALENDAR: CalendarConfig,
}