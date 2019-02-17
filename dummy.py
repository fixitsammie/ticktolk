#!/usr/bin/env python
import os
import sys

def insert_dummy():
    from forum.models import Category
    a=['fashion']
    for i in a:
        Category(name=i).save()
        print("Added Category %s"%i)




if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticktolk.settings")
    insert_dummy()
