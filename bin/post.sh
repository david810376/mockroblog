#!/bin/sh

http --verbose POST localhost:5000/user/ @"$1"
