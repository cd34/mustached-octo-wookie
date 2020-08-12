import os
import configparser
import sys

import libs.methods

config = configparser.ConfigParser()
config.read_file(open("glacierputter.cfg.sample"))


class TestContents:
    def test_existing_contents(self):
        existing_contents = libs.methods.get_local_contents(config)
        assert type(existing_contents) == dict

    def test_existing_files(self):
        existing_contents = libs.methods.get_local_contents(config)

        existing_files = [x["ArchiveDescription"] for x in existing_contents.values()]
        assert type(existing_files) == list

    def test_file(self):
        existing_contents = libs.methods.get_local_contents(config)
        existing_files = [x["ArchiveDescription"] for x in existing_contents.values()]

        assert "test_data.m4v" in existing_files

    def test_id(self):
        existing_contents = libs.methods.get_local_contents(config)

        assert existing_contents.get(
            "FeBDpUkqBFnlDRYu4kNMSWVgBUrur-YLbJG6FiWwuV3iephZCClg6U-smty7rgi2hm8rOFTwnFNFOLvoLqW2Tlgb2V1NLzkVxe71m5OcsD9coOGfju6KRzRjN5gCP4s9IOycOcoIPA"
        )
        assert existing_contents.get("nothere") == None

    def test_update_local_contents(self):
        libs.methods.update_local_contents(config, "1", "test_data/test_data.m4v")

    def test_delete_local_contents(self):
        libs.methods.delete_local_contents(config, "1")
