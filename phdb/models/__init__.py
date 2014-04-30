# -*- coding: utf-8 -*-
import hashlib
import sqlalchemy as sa
from phdb.models.common import meta

__author__ = 'Victor Poluksht'

records_id_seq = sa.Sequence('records_id_sequence')

class Record(meta):
    __tablename__ = 'records'

    id = sa.Column('id', sa.types.Integer, sa.Sequence(records_id_seq), primary_key=True)
    code = sa.Column('code', sa.types.Integer, nullable=False)
    nfrom = sa.Column('nfrom', sa.types.Integer, nullable=False)
    nto = sa.Column('nto', sa.types.Integer, nullable=False)
    amount = sa.Column('amount', sa.types.Integer, nullable=False)
    operator = sa.Column('company', sa.types.Unicode(128), nullable = False)
    region = sa.Column('region', sa.types.Unicode(128), nullable = False)

    def asDict(self):
        return {'id': self.id, 'code': self.code, 'nfrom': self.nfrom,
                'nto': self.nto, 'amount': self.amount,
                'operator': self.operator, 'region': self.region}

    def __eq__(self, other):
        if self.code == other.code and self.nfrom == other.nfrom and self.nto == other.nto:
            return True
        return False

    def __hash__(self):
        return hash(self.code + self.nfrom + self.nto)