from geopulse.config import load_settings


def test_default_environment_is_dev(monkeypatch) -> None:
    monkeypatch.delenv("GEOPULSE_ENV", raising=False)

    settings = load_settings()

    assert settings.environment == "dev"


def test_environment_can_be_overridden(monkeypatch) -> None:
    monkeypatch.setenv("GEOPULSE_ENV", "test")

    settings = load_settings()

    assert settings.environment == "test"
