# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
import mock


paramiko = 'openerp.addons.connector_sftp.models.connector_sftp.paramiko'


class TestConnectorSftp(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestConnectorSftp, self).setUp(*args, **kwargs)
        self.model_obj = self.env['connector.sftp']
        self.vals = {
            'name': 'Test',
            'host': 'example.com',
            'port': 22,
            'username': 'test',
            'password': 'pass',
            'host_key': 'hostkey',
            'private_key': 'privatekey',
            'company_id': self.env.user.company_id.id,
        }

    def _new_record(self, ):
        return self.model_obj.create(self.vals)

    @mock.patch(paramiko)
    def test_create_client_initializes_transport(self, mk):
        rec_id = self._new_record()
        rec_id._create_client()
        mk.Transport.assert_called_once_with((
            self.vals['host'], self.vals['port']
        ))

    @mock.patch(paramiko)
    def test_create_client_connects_to_transport(self, mk):
        rec_id = self._new_record()
        rec_id._create_client()
        mk.Transport().connect.assert_called_once_with(
            hostkey=self.vals['host_key'],
            username=self.vals['username'],
            password=self.vals['password'],
            pkey=self.vals['private_key'],
        )

    @mock.patch(paramiko)
    def test_create_client_inits_sftp_client(self, mk):
        rec_id = self._new_record()
        rec_id._create_client()
        mk.SFTPClient.from_transport.assert_called_once_with(
            mk.Transport()
        )

    @mock.patch(paramiko)
    def test_sftp_listdir(self, mk):
        rec_id = self._new_record()
        expect = 'Test'
        rec_id._sftp_listdir(expect)
        rec_id.client.listdir.assert_called_once_with(expect)

    @mock.patch(paramiko)
    def test_sftp_stat(self, mk):
        rec_id = self._new_record()
        expect = 'Test'
        rec_id._sftp_stat(expect)
        rec_id.client.stat.assert_called_once_with(expect)

    @mock.patch(paramiko)
    def test_sftp_open(self, mk):
        rec_id = self._new_record()
        expect = 'Test', 'w', 1
        rec_id._sftp_open(*expect)
        rec_id.client.open.assert_called_once_with(*expect)

    @mock.patch(paramiko)
    def test_sftp_unlink(self, mk):
        rec_id = self._new_record()
        expect = 'Test'
        rec_id._sftp_unlink(expect)
        rec_id.client.unlink.assert_called_once_with(expect)

    @mock.patch(paramiko)
    def test_sftp_symlink(self, mk):
        rec_id = self._new_record()
        expect = 'Test', 'Dest'
        rec_id._sftp_symlink(*expect)
        rec_id.client.symlink.assert_called_once_with(*expect)
