#!/bin/bash

nmcli connection reload eth0
nmcli connection down eth0
nmcli connection up eth0
