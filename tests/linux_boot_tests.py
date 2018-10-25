#!/usr/bin/env python3

import unittest
import pytest
import os
import subprocess
import sys

# Do not allow generating binary artifacts
sys.dont_write_bytecode = True

def test_linux_boot(output_dir, vharness):
    linux_cfg = os.path.join(output_dir, 'bbl-vmlinux0.cfg')
    cmd = [vharness, linux_cfg, '--terminate-event', 'linux-boot']
    print(" ".join(cmd))
    subprocess.check_call(cmd, timeout=600)


def test_linux_checkpoint_create(output_dir, vharness):
    linux_cfg = os.path.join(output_dir, 'bbl-vmlinux0.cfg')
    chpt_filename = os.path.join(output_dir, 'linux-checkpoint.snap')
    checkpoint_cmd = [vharness, '--save', chpt_filename,
                      '--maxinsns', '150000000', linux_cfg]
    print(" ".join(checkpoint_cmd))
    subprocess.run(checkpoint_cmd, stdout=sys.stdout, stderr=sys.stderr,
                   check=True, timeout=600)
    restore_cmd = [vharness, '--load', chpt_filename, linux_cfg,
                   '--terminate-event', 'linux-boot']
    print(" ".join(restore_cmd))
    subprocess.check_call(restore_cmd, timeout=600)
