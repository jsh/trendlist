"""Tests for count_trends."""


from count_trends import (  # import the module to be tested
    all_trendlists,
    count_trends,
    perms,
    single_trends,
    stirlings,
    sum_and_weighted_mean,
    trend_counts,
    uphills,
)


def test_perms():
    """Test perms() function."""
    assert perms([1, 2, 3]) == [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert perms([1, 2, 3, 4]) == [
        [1, 2, 3, 4],
        [1, 2, 4, 3],
        [1, 3, 2, 4],
        [1, 3, 4, 2],
        [1, 4, 2, 3],
        [1, 4, 3, 2],
        [2, 1, 3, 4],
        [2, 1, 4, 3],
        [2, 3, 1, 4],
        [2, 3, 4, 1],
        [2, 4, 1, 3],
        [2, 4, 3, 1],
        [3, 1, 2, 4],
        [3, 1, 4, 2],
        [3, 2, 1, 4],
        [3, 2, 4, 1],
        [3, 4, 1, 2],
        [3, 4, 2, 1],
        [4, 1, 2, 3],
        [4, 1, 3, 2],
        [4, 2, 1, 3],
        [4, 2, 3, 1],
        [4, 3, 1, 2],
        [4, 3, 2, 1],
    ]


def test_all_trendlists():
    """Test all_trendlists() function."""
    assert all_trendlists([1, 2, 4]) == [
        [[1, 2, 4]],
        [[1, 4], [2]],
        [[2, 1, 4]],
        [[2, 4], [1]],
        [[4], [1, 2]],
        [[4], [2], [1]],
    ]


def test_count_trends():
    """Test count_trends() function."""
    trendlists = all_trendlists([1, 2, 4])
    assert count_trends(trendlists) == [1, 2, 1, 2, 2, 3]
    trendlists = all_trendlists([1, 2, 4, 8])
    assert count_trends(trendlists) == [
        1,
        1,
        1,
        2,
        2,
        3,
        1,
        1,
        1,
        2,
        2,
        3,
        2,
        2,
        2,
        2,
        2,
        3,
        2,
        3,
        2,
        3,
        3,
        4,
    ]


def test_trend_counts():
    """Test trend_counts() function."""
    trendlists = all_trendlists([1, 2, 4])
    assert trend_counts(trendlists) == [0, 2, 3, 1]
    trendlists = all_trendlists([1, 2, 4, 8])
    assert trend_counts(trendlists) == [0, 6, 11, 6, 1]


def test_stirlings():
    """Test stirlings() function."""
    assert stirlings(3) == [0, 2, 3, 1]
    assert stirlings(4) == [0, 6, 11, 6, 1]
    assert stirlings(5) == [0, 24, 50, 35, 10, 1]
    assert stirlings(6) == [0, 120, 274, 225, 85, 15, 1]


def test_single_trends():
    """Test single_trends() function."""
    trendlists = all_trendlists([1, 2, 4])
    assert single_trends(trendlists) == [[1, 2, 4], [2, 1, 4]]

    trendlists = all_trendlists([1, 2, 4, 8])
    assert single_trends(trendlists) == [
        [1, 2, 4, 8],
        [1, 2, 8, 4],
        [1, 4, 2, 8],
        [2, 1, 4, 8],
        [2, 1, 8, 4],
        [2, 4, 1, 8],
    ]


def test_sum_and_weighted_mean():
    """Test sum_and_weighted_mean() function."""
    assert sum_and_weighted_mean([1, 2, 3, 4]) == (10, 2.0)


def test_uphills():
    """Test uphills() function."""
    assert uphills([[[1, 2, 4, 8, 16]]]) == [[[16], [8], [4], [2], [1]]]
    assert uphills([[[1, 2, 4, 8]]]) == [[[8], [4], [2], [1]]]
    assert uphills([[[1, 2, 8, 4]]]) == [[[4, 8], [2], [1]]]
    assert uphills([[[1, 4, 2, 8]]]) == [[[8], [2, 4], [1]]]
    assert uphills([[[2, 1, 4, 8]]]) == [[[8], [4], [1, 2]]]
    assert uphills([[[2, 1, 8, 4]]]) == [[[4, 8], [1, 2]]]
    assert uphills([[[2, 4, 1, 8]]]) == [[[8], [1, 4], [2]]]
