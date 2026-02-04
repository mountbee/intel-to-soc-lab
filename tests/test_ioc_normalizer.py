from tools.ioc_normalizer.ioc_normalizer import (
    classify_ioc,
    deduplicate,
    normalize_value,
)


def test_classify_ioc_types():
    assert classify_ioc("203.0.113.10") == "ip"
    assert classify_ioc("example.com") == "domain"
    assert classify_ioc("http://example.com/path") == "url"
    assert classify_ioc("d41d8cd98f00b204e9800998ecf8427e") == "hash_md5"
    assert classify_ioc("da39a3ee5e6b4b0d3255bfef95601890afd80709") == "hash_sha1"
    assert (
        classify_ioc(
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )
        == "hash_sha256"
    )
    assert classify_ioc("user@example.com") == "email"
    assert classify_ioc("not_an_ioc") == "unknown"


def test_normalize_domain_and_url():
    assert normalize_value("ExAmPle.COM", "domain") == "example.com"
    assert (
        normalize_value("HTTP://Example.COM/Path?Q=1", "url")
        == "http://example.com/Path?Q=1"
    )


def test_normalize_url_lowercase_host():
    assert (
        normalize_value("https://EXAMPLE.COM/SomePath", "url")
        == "https://example.com/SomePath"
    )


def test_deduplicate_case_insensitive():
    records = [
        {
            "type": "domain",
            "value": "example.com",
            "source": "s",
            "confidence": 3,
        },
        {
            "type": "domain",
            "value": "Example.COM",
            "source": "s",
            "confidence": 3,
        },
        {
            "type": "ip",
            "value": "203.0.113.10",
            "source": "s",
            "confidence": 3,
        },
        {
            "type": "ip",
            "value": "203.0.113.10",
            "source": "s",
            "confidence": 3,
        },
        {
            "type": "email",
            "value": "User@Example.com",
            "source": "s",
            "confidence": 3,
        },
        {
            "type": "email",
            "value": "user@example.com",
            "source": "s",
            "confidence": 3,
        },
    ]
    deduped = deduplicate(records)
    assert len(deduped) == 3
