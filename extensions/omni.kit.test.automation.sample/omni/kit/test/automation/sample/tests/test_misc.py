# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary

import unittest

from omni.kit.test.automation.sample.endpoints.misc import _is_valid_image_path


class TestScreenshotPathValidation(unittest.TestCase):
    def test_valid_png_and_jpeg_extensions(self):
        self.assertTrue(_is_valid_image_path("/tmp/screenshot.png"))
        self.assertTrue(_is_valid_image_path("C:/users/user/screenshot.jpeg"))

    def test_invalid_extensions_rejected(self):
        self.assertFalse(_is_valid_image_path("/tmp/screenshot_png.exe"))
        self.assertFalse(_is_valid_image_path("/tmp/jpeg/malicious.txt"))
        self.assertFalse(_is_valid_image_path("/tmp/screenshot"))
        self.assertFalse(_is_valid_image_path("/tmp/screenshot.jpg"))

    def test_extension_check_is_case_insensitive(self):
        self.assertTrue(_is_valid_image_path("/tmp/screenshot.PNG"))
        self.assertTrue(_is_valid_image_path("/tmp/screenshot.JPEG"))

    def test_malicious_directory_name_not_accepted(self):
        self.assertFalse(_is_valid_image_path("/tmp/png_dir/screenshot"))
        self.assertFalse(_is_valid_image_path("/tmp/jpeg_dir/screenshot.txt"))


