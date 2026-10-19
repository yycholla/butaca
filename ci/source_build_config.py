"""Backend identity carried from a release build into its isolated reconstruction."""


def release_configuration(environment):
    # Make's $(if $(JELLYFIN),...) treats every nonempty value (even "0") as on.
    jellyfin = "1" if environment.get("JELLYFIN") else ""
    return {
        "RELEASE": "1",
        "FLAVOR": "stable",
        "JELLYFIN": jellyfin,
        "features": "no-default-features" + (" --features jellyfin" if jellyfin else ""),
        "private_telemetry": "excluded; reconstruction defaults without endpoints",
    }


def jellyfin_make_argument(configuration):
    # Older bundles predate this field and describe a Plex build. Always pass an
    # explicit make argument so the caller's environment cannot change the backend.
    jellyfin = configuration.get("JELLYFIN", "")
    if jellyfin not in ("", "1"):
        raise ValueError("source bundle has an unsupported Jellyfin configuration")
    expected = "no-default-features" + (" --features jellyfin" if jellyfin else "")
    if configuration.get("features") != expected:
        raise ValueError("source bundle feature list disagrees with its Jellyfin setting")
    return "JELLYFIN=" + jellyfin
