#!/usr/bin/env python3

from setuptools import setup
import os

setup(
    name="Planus Justitiam",
    description="A compressed flat-file store for JSON",
    version="0.2",
    author="Hannah Ward",
    author_email="hannah.ward2@baesystems.com",
    packages=['planus'],
    install_requires=["pylzma", "nose"]
)
