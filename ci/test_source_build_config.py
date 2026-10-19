import unittest

from source_build_config import jellyfin_make_argument, release_configuration


class BackendReconstruction(unittest.TestCase):
    def test_jellyfin_survives_record_and_restore(self):
        config = release_configuration({"JELLYFIN": "1"})
        self.assertEqual(config["features"], "no-default-features --features jellyfin")
        self.assertEqual(jellyfin_make_argument(config), "JELLYFIN=1")

    def test_plex_explicitly_overrides_an_inherited_jellyfin_environment(self):
        self.assertEqual(jellyfin_make_argument(release_configuration({})), "JELLYFIN=")

    def test_nonempty_make_values_enable_the_backend(self):
        self.assertEqual(release_configuration({"JELLYFIN": "0"})["JELLYFIN"], "1")

    def test_old_plex_manifest_stays_plex(self):
        self.assertEqual(jellyfin_make_argument({"features": "no-default-features"}), "JELLYFIN=")

    def test_disagreement_is_refused(self):
        with self.assertRaises(ValueError):
            jellyfin_make_argument({"JELLYFIN": "1", "features": "no-default-features"})

    def test_unknown_value_is_refused(self):
        with self.assertRaises(ValueError):
            jellyfin_make_argument({"JELLYFIN": "other", "features": "no-default-features"})

    def test_unrelated_environment_is_not_recorded(self):
        self.assertNotIn("SERVER_PASSWORD", release_configuration({"SERVER_PASSWORD": "synthetic"}))


if __name__ == "__main__":
    unittest.main()
