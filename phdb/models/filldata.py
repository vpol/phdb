# -*- coding: utf-8 -*-
from datetime import datetime, date
import logging
import transaction

__author__ = 'Victor Poluksht'

log = logging.getLogger(__name__)

def populate():
    
    from phdb.models.common import meta

    transaction.commit()
