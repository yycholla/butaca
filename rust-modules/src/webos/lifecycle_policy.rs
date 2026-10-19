//! Lifecycle ownership compatibility for the TV's SDL initialization.

/// Preserve SDL's lifecycle ownership on webOS 6. On the tested 6.5.3 firmware,
/// the early custom claim leaves SDL with an anonymous bus connection and its
/// panel-resolution request fails; SDL then waits indefinitely. Keeping the
/// established policy elsewhere avoids changing other firmware without evidence.
pub(crate) fn claim_before_sdl(webos_major: u32) -> bool {
    webos_major != 6
}

#[cfg(test)]
mod tests {
    use super::claim_before_sdl;

    #[test]
    fn webos6_keeps_sdl_as_the_lifecycle_owner() {
        assert!(!claim_before_sdl(6));
    }

    #[test]
    fn other_firmware_keeps_the_existing_policy() {
        for major in [0, 4, 5, 7, 10, 11] {
            assert!(claim_before_sdl(major), "unexpected change for webOS {major}");
        }
    }
}
