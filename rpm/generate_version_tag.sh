#!/bin/sh -e
# SPDX-FileCopyrightText: 2023, Jolla Ltd.
# SPDX-License-Identifier: GPL-2.0

# Version tag is based upon:
# original upstream version + counts of commits on upstream
# https://github.com/archlinux/svntogit-packages/blob/packages/vpnc/trunk/PKGBUILD#L31

printf "%s.r%s" "$(grep '^VERSION' upstream/Makefile|sed 's|VERSION := ||')" \
       "$(git -C upstream rev-list --count HEAD)"
