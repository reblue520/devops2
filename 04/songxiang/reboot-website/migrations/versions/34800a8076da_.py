"""empty message

Revision ID: 34800a8076da
Revises: 12c3bdc2b4a1
Create Date: 2016-05-29 11:55:10.947609

"""

# revision identifiers, used by Alembic.
revision = '34800a8076da'
down_revision = '12c3bdc2b4a1'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('management_card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('m_type', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('m_type')
    )
    op.create_table('manufacturers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('power',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server_power', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('server_power')
    )
    op.create_table('server',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('supplier', sa.String(length=400), nullable=True),
    sa.Column('manufacturers', sa.String(length=100), nullable=True),
    sa.Column('manufacture_date', sa.Date(), nullable=True),
    sa.Column('server_type', sa.String(length=50), nullable=True),
    sa.Column('st', sa.String(length=50), nullable=True),
    sa.Column('assets_no', sa.String(length=50), nullable=True),
    sa.Column('idc_id', sa.String(length=32), nullable=True),
    sa.Column('cabinet_id', sa.Integer(), nullable=True),
    sa.Column('uuid', sa.String(length=50), nullable=True),
    sa.Column('cabinet_pos', sa.String(length=15), nullable=True),
    sa.Column('expire', sa.Date(), nullable=True),
    sa.Column('ups', sa.Integer(), nullable=True),
    sa.Column('parter', sa.String(length=50), nullable=True),
    sa.Column('parter_type', sa.String(length=50), nullable=True),
    sa.Column('server_up_time', sa.Date(), nullable=True),
    sa.Column('os', sa.String(length=50), nullable=True),
    sa.Column('hostname', sa.String(length=30), nullable=True),
    sa.Column('inner_ip', sa.String(length=50), nullable=True),
    sa.Column('mac_address', sa.String(length=50), nullable=True),
    sa.Column('ipinfo', sa.String(length=50), nullable=True),
    sa.Column('server_cpu', sa.String(length=50), nullable=True),
    sa.Column('server_disk', sa.String(length=50), nullable=True),
    sa.Column('server_mem', sa.String(length=50), nullable=True),
    sa.Column('raid', sa.String(length=50), nullable=True),
    sa.Column('raid_card_type', sa.String(length=50), nullable=True),
    sa.Column('remote_card', sa.String(length=50), nullable=True),
    sa.Column('remote_cardip', sa.String(length=50), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('remark', sa.Text(), nullable=True),
    sa.Column('last_op_time', sa.DateTime(), nullable=True),
    sa.Column('last_op_people', sa.Integer(), nullable=True),
    sa.Column('monitor_mail_group', sa.String(length=50), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('server_purpose', sa.Integer(), nullable=True),
    sa.Column('trouble_resolve', sa.Integer(), nullable=True),
    sa.Column('op_interface_other', sa.Integer(), nullable=True),
    sa.Column('dev_interface', sa.Integer(), nullable=True),
    sa.Column('check_update_time', sa.DateTime(), nullable=True),
    sa.Column('vm_status', sa.Integer(), nullable=True),
    sa.Column('power', sa.String(length=30), nullable=True),
    sa.Column('host', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_server_cabinet_id'), 'server', ['cabinet_id'], unique=False)
    op.create_index(op.f('ix_server_hostname'), 'server', ['hostname'], unique=False)
    op.create_index(op.f('ix_server_idc_id'), 'server', ['idc_id'], unique=False)
    op.create_index(op.f('ix_server_inner_ip'), 'server', ['inner_ip'], unique=False)
    op.create_index(op.f('ix_server_os'), 'server', ['os'], unique=False)
    op.create_index(op.f('ix_server_uuid'), 'server', ['uuid'], unique=False)
    op.create_index(op.f('ix_server_vm_status'), 'server', ['vm_status'], unique=False)
    op.create_table('server_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('manufacturers_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_server_type_manufacturers_id'), 'server_type', ['manufacturers_id'], unique=False)
    op.drop_table('manufactures')
    op.drop_table('Servertype')
    op.create_index(op.f('ix_cabinet_idc_id'), 'cabinet', ['idc_id'], unique=False)
    op.create_index(op.f('ix_product_pid'), 'product', ['pid'], unique=False)
    op.drop_index('dev_interface', table_name='product')
    op.drop_index('module_letter', table_name='product')
    op.drop_index('op_interface', table_name='product')
    op.drop_index('pid', table_name='product')
    op.drop_index('service_name', table_name='product')
    op.alter_column(u'raid', 'name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=True)
    op.alter_column(u'raidtype', 'name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column(u'supplier', 'name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(u'supplier', 'name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column(u'raidtype', 'name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column(u'raid', 'name',
               existing_type=mysql.VARCHAR(length=20),
               nullable=False)
    op.create_index('service_name', 'product', ['service_name'], unique=True)
    op.create_index('pid', 'product', ['pid'], unique=True)
    op.create_index('op_interface', 'product', ['op_interface'], unique=True)
    op.create_index('module_letter', 'product', ['module_letter'], unique=True)
    op.create_index('dev_interface', 'product', ['dev_interface'], unique=True)
    op.drop_index(op.f('ix_product_pid'), table_name='product')
    op.drop_index(op.f('ix_cabinet_idc_id'), table_name='cabinet')
    op.create_table('Servertype',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('type', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('manufacturers_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.create_table('manufactures',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.drop_index(op.f('ix_server_type_manufacturers_id'), table_name='server_type')
    op.drop_table('server_type')
    op.drop_index(op.f('ix_server_vm_status'), table_name='server')
    op.drop_index(op.f('ix_server_uuid'), table_name='server')
    op.drop_index(op.f('ix_server_os'), table_name='server')
    op.drop_index(op.f('ix_server_inner_ip'), table_name='server')
    op.drop_index(op.f('ix_server_idc_id'), table_name='server')
    op.drop_index(op.f('ix_server_hostname'), table_name='server')
    op.drop_index(op.f('ix_server_cabinet_id'), table_name='server')
    op.drop_table('server')
    op.drop_table('power')
    op.drop_table('manufacturers')
    op.drop_table('management_card')
    ### end Alembic commands ###
