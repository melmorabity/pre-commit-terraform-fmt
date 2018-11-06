# -*- coding: utf-8 -*-

"""Unit testing module for pre-commit-terraform-fmt."""


import os
import filecmp

import pytest

import terraform.fmt

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.mark.datafiles(os.path.join(DATA_DIR, "ok", "formatted"))
def test_terraform_fmt_formatted(datafiles):
    """Verify that valid and well-formatted Terraform files are successfully
    parsed and not modified."""

    return_code = terraform.fmt.run(datafiles.listdir())
    assert return_code == 0

    # Ensure files haven't changed after formatting
    dircmp = filecmp.dircmp(
        os.path.join(DATA_DIR, "ok", "formatted"), datafiles.strpath
    )
    assert not dircmp.diff_files
    assert dircmp.same_files


@pytest.mark.datafiles(os.path.join(DATA_DIR, "ok", "unformatted"))
def test_terraform_fmt_unformatted(datafiles):
    """Verify that valid and unformatted Terraform files are successfully
    parsed and modified."""

    return_code = terraform.fmt.run(datafiles.listdir())
    assert return_code != 0

    # Ensure files have changed after formatting
    dircmp = filecmp.dircmp(
        os.path.join(DATA_DIR, "ok", "unformatted"), datafiles.strpath
    )
    assert dircmp.diff_files
    assert not dircmp.same_files

    # Compare resulting files with expected results
    dircmp = filecmp.dircmp(
        os.path.join(DATA_DIR, "ok", "formatted"), datafiles.strpath
    )
    assert not dircmp.diff_files
    assert dircmp.same_files


@pytest.mark.datafiles(os.path.join(DATA_DIR, "ko"))
def test_terraform_fmt_ko(datafiles):
    """Verify that invalid Terraform files are not modified."""

    return_code = terraform.fmt.run(datafiles.listdir())
    assert return_code != 0

    # Ensure files haven't changed after formatting attempt
    dircmp = filecmp.dircmp(os.path.join(DATA_DIR, "ko"), datafiles.strpath)
    assert not dircmp.diff_files
    assert dircmp.same_files


@pytest.mark.datafiles(os.path.join(DATA_DIR, "ok"))
def test_terraform_no_bin(datafiles):
    """Checks invalid Terraform paths."""

    # No such file
    return_code = terraform.fmt.run(
        datafiles.listdir(), terraform=datafiles.strpath
    )
    assert return_code != 0

    # Permission denied
    return_code = terraform.fmt.run(datafiles.listdir(), terraform="/dev/null")
    assert return_code != 0
