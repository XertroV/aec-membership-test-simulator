#!/usr/bin/env bash
pandoc -f markdown -t html --standalone -o index.html README.md --metadata pagetitle="Simulate AEC Membership Test"
