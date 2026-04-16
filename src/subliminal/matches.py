"""Get matches between a :class:`~subliminal.video.Video` object and a dict of guesses.

.. py:function:: guess_matches(video, guess, *, partial = False)

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param guess: the guess.
    :type guess: dict[str, Any]
    :param bool partial: whether or not the guess is partial.
    :return: matches between the `video` and the `guess`.
    :rtype: set[str]

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .score import get_equivalent_release_groups, score_keys
from .utils import ensure_list, sanitize, sanitize_release_group
from .video import Episode, Movie, Video

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Protocol

    from babelfish import Country  # type: ignore[import-untyped]

    class MatchingFunc(Protocol):
        """Match a :class:`~subliminal.video.Video` to criteria."""

        def __call__(self, video: Video, **kwargs: Any) -> bool: ...  # noqa: D102


def series_matches(video: Video, *, title: str | None = None, **kwargs: Any) -> bool:
    """Whether the `video` matches the series title.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str title: the series name.
    :return: whether there's a match
    :rtype: bool

    """
    pass


def title_matches(video: Video, *, title: str | None = None, episode_title: str | None = None, **kwargs: Any) -> bool:
    """Whether the movie matches the movie `title` or the series matches the `episode_title`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str title: the movie title.
    :param str episode_title: the series episode title.
    :return: whether there's a match
    :rtype: bool

    """
    pass


def season_matches(video: Video, *, season: int | None = None, **kwargs: Any) -> bool:
    """Whether the episode matches the `season`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param int season: the episode season.
    :return: whether there's a match
    :rtype: bool

    """
    pass


def episode_matches(video: Video, *, episode: int | None = None, **kwargs: Any) -> bool:
    """Whether the episode matches the `episode`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param episode: the episode season.
    :type: list of int or int
    :return: whether there's a match
    :rtype: bool

    """
    pass


def year_matches(video: Video, *, year: int | None = None, partial: bool = False, **kwargs: Any) -> bool:
    """Whether the video matches the `year`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param int year: the video year.
    :param bool partial: whether or not the guess is partial.
    :return: whether there's a match
    :rtype: bool

    """
    pass


def country_matches(video: Video, *, country: Country | None = None, partial: bool = False, **kwargs: Any) -> bool:
    """Whether the video matches the `country`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param country: the video country.
    :type country: :class:`~babelfish.country.Country`
    :param bool partial: whether or not the guess is partial.
    :return: whether there's a match
    :rtype: bool

    """
    pass


def fps_matches(video: Video, *, fps: float | None = None, strict: bool = True, **kwargs: Any) -> bool:
    """Whether the video matches the `fps`.

    Frame rates are considered equal if the relative difference is less than 0.1 percent.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str fps: the video frame rate.
    :param bool strict: if strict, an absence of information is a non-match.
    :return: whether there's a match
    :rtype: bool

    """
    # make the difference a bit more than 0.1% to be sure
    relative_diff = 0.0011
    # if video and subtitle fps are defined, return True if the match, otherwise False
    if video.frame_rate is not None and video.frame_rate > 0 and fps is not None and fps > 0:
        return bool(abs(video.frame_rate - fps) / video.frame_rate < relative_diff)

    # if information is missing, return True only if not strict
    return not strict


def release_group_matches(video: Video, *, release_group: str | None = None, **kwargs: Any) -> bool:
    """Whether the video matches the `release_group`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str release_group: the video release group.
    :return: whether there's a match
    :rtype: bool

    """
    pass


def streaming_service_matches(video: Video, *, streaming_service: str | None = None, **kwargs: Any) -> bool:
    """Whether the video matches the `streaming_service`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str streaming_service: the video streaming service
    :return: whether there's a match
    :rtype: bool

    """
    pass


def resolution_matches(video: Video, *, screen_size: str | None = None, **kwargs: Any) -> bool:
    """Whether the video matches the `resolution`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str screen_size: the video resolution
    :return: whether there's a match
    :rtype: bool

    """
    pass


def source_matches(video: Video, *, source: str | None = None, **kwargs: Any) -> bool:
    """Whether the video matches the `source`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str source: the video source
    :return: whether there's a match
    :rtype: bool

    """
    pass


def video_codec_matches(video: Video, *, video_codec: str | None = None, **kwargs: Any) -> bool:
    """Whether the video matches the `video_codec`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str video_codec: the video codec
    :return: whether there's a match
    :rtype: bool

    """
    pass


def audio_codec_matches(video: Video, *, audio_codec: str | None = None, **kwargs: Any) -> bool:
    """Whether the video matches the `audio_codec`.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param str audio_codec: the video audio codec
    :return: whether there's a match
    :rtype: bool

    """
    pass


#: Available matches functions
matches_manager: dict[str, MatchingFunc] = {
    'series': series_matches,
    'title': title_matches,
    'season': season_matches,
    'episode': episode_matches,
    'year': year_matches,
    'country': country_matches,
    'fps': fps_matches,
    'release_group': release_group_matches,
    'streaming_service': streaming_service_matches,
    'resolution': resolution_matches,
    'source': source_matches,
    'video_codec': video_codec_matches,
    'audio_codec': audio_codec_matches,
}


def guess_matches(video: Video, guess: Mapping[str, Any], *, partial: bool = False, strict: bool = True) -> set[str]:
    """Get matches between a `video` and a `guess`.

    If a guess is `partial`, the absence of information won't be counted as a match.
    If a match is `strict`, the absence of information will be counted as a non-match.

    :param video: the video.
    :type video: :class:`~subliminal.video.Video`
    :param guess: the guess.
    :type guess: dict
    :param bool partial: whether or not the guess is partial.
    :param bool strict: whether or not the match is strict.
    :return: matches between the `video` and the `guess`.
    :rtype: set

    """
    matches = set()
    for key in score_keys:
        if key in matches_manager and matches_manager[key](video, partial=partial, strict=strict, **guess):
            matches.add(key)

    return matches
