# Native Jellyfin build for LG 55UP7670PUC

This checkout starts from [Butaca](https://github.com/gnacho/butaca), the Jellyfin
fork of [PlxNative](https://github.com/GLinnik21/plx-native). It reuses their native
Rust interface, GPU rendering and webOS playback implementation. This is not an
independent rewrite. Keep the GPL license and third-party notices with any copies.

The target TV is an LG 55UP7670PUC, originally supplied with webOS 6.0. Compatibility
and performance on this particular TV have not been tested. Static firmware checks
and host unit tests do not establish that video works on the physical TV.

## Build with GitHub Actions

1. Put this checkout in a repository in your own GitHub account.
2. Open **Actions → Personal Jellyfin TV build → Run workflow** on the branch with
   these changes. The workflow needs an available `ubuntu-24.04-arm` runner for the
   package job. No Jellyfin credentials or TV network access are needed by CI.
3. Wait for both jobs to finish successfully. Download the
   **jellyfin-webos-tv-package** artifact. It contains the `.ipk` package, build
   configuration, compatibility evidence and corresponding source.

The workflow uses `JELLYFIN=1`, `FLAVOR=stable` and `RELEASE=1` through the existing
shared packaging workflow. It builds app ID `com.butaca`, titled **Butaca**. It does
not publish a GitHub release or install anything on the TV. Installing that ID
would update any existing Butaca installation; check first. The official Jellyfin
app has a separate ID.

For a supported local build host (macOS or ARM64 Linux), follow
[building.md](building.md), then run:

```sh
make setup-env
make FLAVOR=stable RELEASE=1 JELLYFIN=1 ipk
```

Do not omit `JELLYFIN=1`: this inherited Makefile still defaults to the Plex backend.

## TV setup and approval

Check for an LG **Developer Mode** app from the Home screen. Opening it to inspect
its status does not enable it. Before enabling Developer Mode, installing a package,
changing a setting or restarting, ask the owner to approve that specific change.
Follow LG's Developer Mode process and webOS Dev Manager for an unrooted TV; do not
use the repository's root SSH deploy targets on a stock TV. Developer Mode sessions
need renewal, and expiry can remove sideloaded apps.

On first launch, the Jellyfin form asks for server URL, username and password.
Enter credentials on the TV; do not commit them or supply them to Actions. This
base currently persists the account password in its TV configuration for automatic
sign-in, rather than retaining only an access token. Review that behavior before
installation. Plain HTTP authentication is restricted to private LAN IP addresses;
use HTTPS for a remote server or hostname.

## Acceptance on the actual TV

Record any available memory reading before installing; distinguish RAM from app
storage. If stock Developer Mode does not expose a measurement, report it as
unavailable instead of estimating. After approved installation, check sign-in,
remote navigation, library artwork, a representative movie and episode, seeking,
audio, subtitles, resume and progress. Playback and progress reporting change the
server's viewing record, so use an owner-approved test account or library.

After the last approved TV change, wait 30 seconds. Ask before the single restart,
then confirm normal Home, inputs and app startup and repeat the same memory reading.
Keep a dated log of exact prior settings and undo steps for every approved change.
No cleanup, app disabling, launcher replacement or screensaver changes are part of
this build.

Current TV change log: **none**. No connection, installation or memory measurement
has been performed.
