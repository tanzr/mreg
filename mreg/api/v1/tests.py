from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from mreg.models import (Cname, HinfoPreset, Host, Ipaddress, NameServer,
                         Naptr, PtrOverride, Srv, Network, Txt, ForwardZone,
                         ReverseZone, ModelChangeLog)

from mreg.utils import create_serialno

def clean_and_save(entity):
    entity.full_clean()
    entity.save()


class ModelHostsTestCase(TestCase):
    """This class defines the test suite for the Host model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org',
                             ttl=300,
                             loc='23 58 23 N 10 43 50 E 80m',
                             comment='some comment')

    def test_model_can_create_a_host(self):
        """Test that the model is able to create a host."""
        old_count = Host.objects.count()
        clean_and_save(self.host_one)
        new_count = Host.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_a_host(self):
        """Test that the model is able to change a host."""
        clean_and_save(self.host_one)
        old_name = self.host_one.name
        new_name = 'some-new-host.example.org'
        host_sample_id = Host.objects.get(name=old_name).id
        self.host_one.name = new_name
        clean_and_save(self.host_one)
        updated_name = Host.objects.get(pk=host_sample_id).name
        self.assertEqual(new_name, updated_name)

    def test_model_can_delete_a_host(self):
        """Test that the model is able to delete a host."""
        clean_and_save(self.host_one)
        old_count = Host.objects.count()
        self.host_one.delete()
        new_count = Host.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_host_can_alter_loc(self):
        """
        Test that the model can validate and store all examples
        from RFC1876, section 4 "Example data".
        """
        clean_and_save(self.host_one)
        for loc in ('42 21 54 N 71 06 18 W -24m 30m',
                    '42 21 43.952 N 71 5 6.344 W -24m 1m 200m',
                    '52 14 05 N 00 08 50 E 10m',
                    '32 7 19 S 116 2 25 E 10m',
                    '42 21 28.764 N 71 00 51.617 W -44m 2000m'):
            self.host_one.loc = loc
            clean_and_save(self.host_one)


class ModelForwardZoneTestCase(TestCase):
    """This class defines the test suite for the ForwardZone model."""

    # TODO: test this for sub-zones (sub.example.org)
    def setUp(self):
        """Define the test client and other test variables."""
        self.zone_sample = ForwardZone(name='example.org',
                                       primary_ns='ns.example.org',
                                       email='hostmaster@example.org',
                                       serialno=1234567890,
                                       refresh=400,
                                       retry=300,
                                       expire=800,
                                       ttl=300)

    def test_model_can_create_a_zone(self):
        """Test that the model is able to create a zone."""
        old_count = ForwardZone.objects.count()
        clean_and_save(self.zone_sample)
        new_count = ForwardZone.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_a_zone(self):
        """Test that the model is able to change a zone."""
        clean_and_save(self.zone_sample)
        old_name = self.zone_sample.name
        new_name = 'example.com'
        zone_sample_id = ForwardZone.objects.get(name=old_name).id
        self.zone_sample.name = new_name
        clean_and_save(self.zone_sample)
        updated_name = ForwardZone.objects.get(pk=zone_sample_id).name
        self.assertEqual(new_name, updated_name)

    def test_model_can_delete_a_zone(self):
        """Test that the model is able to delete a zone."""
        clean_and_save(self.zone_sample)
        old_count = ForwardZone.objects.count()
        self.zone_sample.delete()
        new_count = ForwardZone.objects.count()
        self.assertNotEqual(old_count, new_count)


class ModelNameServerTestCase(TestCase):
    """This class defines the test suite for the NameServer model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.zone_sample = ForwardZone(name='example.org',
                                       primary_ns='some-ns-server.example.org',
                                       email='hostmaster@example.org')

        clean_and_save(self.zone_sample)

        self.ns_sample = NameServer(name='some-ns-server.example.org',
                                    ttl=300)

    def test_model_can_create_ns(self):
        """Test that the model is able to create an Ns."""
        old_count = NameServer.objects.count()
        clean_and_save(self.ns_sample)
        new_count = NameServer.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_ns(self):
        """Test that the model is able to change an Ns."""
        clean_and_save(self.ns_sample)
        old_name = self.ns_sample.name
        new_name = 'some-new-ns.example.com'
        ns_sample_id = NameServer.objects.get(name=old_name).id
        self.ns_sample.name = new_name
        clean_and_save(self.ns_sample)
        updated_name = NameServer.objects.get(pk=ns_sample_id).name
        self.assertEqual(new_name, updated_name)

    def test_model_can_delete_ns(self):
        """Test that the model is able to delete an Ns."""
        clean_and_save(self.ns_sample)
        old_count = NameServer.objects.count()
        self.ns_sample.delete()
        new_count = NameServer.objects.count()
        self.assertNotEqual(old_count, new_count)


class ModelNetworkTestCase(TestCase):
    """This class defines the test suite for the Network model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.network_sample = Network(range='10.0.0.0/20',
                                    description='some description',
                                    vlan=123,
                                    dns_delegated=False,
                                    category='so',
                                    location='Test location',
                                    frozen=False)

    def test_model_can_create_ns(self):
        """Test that the model is able to create a Network."""
        old_count = Network.objects.count()
        clean_and_save(self.network_sample)
        new_count = Network.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_ns(self):
        """Test that the model is able to change a Network."""
        clean_and_save(self.network_sample)
        new_vlan = 321
        network_sample_id = self.network_sample.id
        self.network_sample.vlan = new_vlan
        clean_and_save(self.network_sample)
        updated_vlan = Network.objects.get(pk=network_sample_id).vlan
        self.assertEqual(new_vlan, updated_vlan)

    def test_model_can_delete_ns(self):
        """Test that the model is able to delete a Network."""
        clean_and_save(self.network_sample)
        old_count = Network.objects.count()
        self.network_sample.delete()
        new_count = Network.objects.count()
        self.assertNotEqual(old_count, new_count)


class ModelIpaddressTestCase(TestCase):
    """This class defines the test suite for the Ipaddress model."""

    def setUp(self):
        """Define the test client and other test variables."""
        # Needs sample host and sample network to test properly
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org',
                             ttl=300,
                             loc='23 58 23 N 10 43 50 E 80m',
                             comment='some comment')

        self.network_sample = Network(range='129.240.202.0/20',
                                    description='some description',
                                    vlan=123,
                                    dns_delegated=False)

        clean_and_save(self.host_one)
        # clean_and_save(self.network_sample) # Needed when network ForeignKey is implemented.

        self.ipaddress_sample = Ipaddress(host=Host.objects.get(name='some-host.example.org'),
                                          ipaddress='129.240.202.123',
                                          macaddress='a4:34:d9:0e:88:b9')

    def test_model_can_create_ipaddress(self):
        """Test that the model is able to create an IP Address."""
        old_count = Ipaddress.objects.count()
        clean_and_save(self.ipaddress_sample)
        new_count = Ipaddress.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_ipaddress(self):
        """Test that the model is able to change an IP Address."""
        clean_and_save(self.ipaddress_sample)
        new_ipaddress = '129.240.202.124'
        self.ipaddress_sample.ipaddress = new_ipaddress
        clean_and_save(self.ipaddress_sample)
        updated_ipaddress = Ipaddress.objects.filter(host__name='some-host.example.org')[0].ipaddress
        self.assertEqual(new_ipaddress, updated_ipaddress)

    def test_model_can_delete_ipaddress(self):
        """Test that the model is able to delete an IP Address."""
        clean_and_save(self.ipaddress_sample)
        old_count = Ipaddress.objects.count()
        self.ipaddress_sample.delete()
        new_count = Ipaddress.objects.count()
        self.assertNotEqual(old_count, new_count)


class ModelPtrOverrideTestCase(TestCase):
    """This class defines the test suite for the PtrOverride model."""

    def setUp(self):
        """Define the test client and other test variables."""
        # Needs sample host to test
        self.host_one = Host(name='host1.example.org',
                             contact='mail@example.org')
        self.host_two = Host(name='host2.example.org',
                        contact='mail@example.org')

        clean_and_save(self.host_one)
        clean_and_save(self.host_two)

        self.ptr_sample = PtrOverride(host=Host.objects.get(name='host1.example.org'),
                                      ipaddress='10.0.0.2')

    def test_model_can_create_ptr(self):
        """Test that the model is able to create a PTR Override."""
        old_count = PtrOverride.objects.count()
        clean_and_save(self.ptr_sample)
        new_count = PtrOverride.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_ptr(self):
        """Test that the model is able to change a PTR Override."""
        clean_and_save(self.ptr_sample)
        new_ptr = '10.0.0.3'
        self.ptr_sample.ipaddress = new_ptr
        clean_and_save(self.ptr_sample)
        updated_ptr = PtrOverride.objects.filter(host__name='host1.example.org').first().ipaddress
        self.assertEqual(new_ptr, updated_ptr)

    def test_model_can_delete_ptr(self):
        """Test that the model is able to delete a PTR Override."""
        clean_and_save(self.ptr_sample)
        old_count = PtrOverride.objects.count()
        self.ptr_sample.delete()
        new_count = PtrOverride.objects.count()
        self.assertNotEqual(old_count, new_count)


    def test_model_updated_by_added_ip(self):
        """Test to check that an PtrOverride is added when two hosts share the same ip.
           Also makes sure that the PtrOverride points to the first host which held the ip."""
        initial_count = PtrOverride.objects.count()
        ip_one = Ipaddress(host=self.host_one, ipaddress='10.0.0.1')
        clean_and_save(ip_one)
        one_count = PtrOverride.objects.count()
        ip_two = Ipaddress(host=self.host_two, ipaddress='10.0.0.1')
        clean_and_save(ip_two)
        ptr =  PtrOverride.objects.first()
        self.assertEqual(ptr.host, self.host_one)
        self.assertEqual(ptr.ipaddress, '10.0.0.1')
        self.assertEqual(initial_count, 0)
        self.assertEqual(initial_count, one_count)
        self.assertEqual(PtrOverride.objects.count(), 1)

    def test_model_add_and_remove_ip(self):
        """Test to check that an PtrOverride is added when two hosts share the same ip.
           Also makes sure that the PtrOverride points to the first host which held the ip."""
        initial_count = PtrOverride.objects.count()
        ip_one = Ipaddress(host=self.host_one, ipaddress='10.0.0.1')
        clean_and_save(ip_one)
        one_count = PtrOverride.objects.count()
        ip_two = Ipaddress(host=self.host_two, ipaddress='10.0.0.1')
        clean_and_save(ip_two)
        two_count = PtrOverride.objects.count()
        ptr =  PtrOverride.objects.first()
        self.assertEqual(ptr.host, self.host_one)
        self.assertEqual(ptr.ipaddress, '10.0.0.1')
        self.assertEqual(initial_count, 0)
        self.assertEqual(initial_count, one_count)
        self.assertEqual(two_count, 1)
        self.host_one.delete()
        self.assertEqual(PtrOverride.objects.count(), 0)

    def test_model_two_ips_no_ptroverrides(self):
        """When three or more hosts all have the same ipaddress and the first host
        host, e.g. the one with the PtrOverride, is deleted, a new PtrOverride is
        not created automatically.
        """
        def _add_ip(host, ipaddress):
            ip = Ipaddress(host=host, ipaddress=ipaddress)
            clean_and_save(ip)
        _add_ip(self.host_one, '10.0.0.1')
        _add_ip(self.host_two, '10.0.0.1')
        host_three = Host(name='host3.example.org',
                        contact='mail@example.org')

        clean_and_save(host_three)
        _add_ip(host_three, '10.0.0.1')
        self.host_one.delete()
        self.assertEqual(PtrOverride.objects.count(), 0)
        self.assertEqual(Ipaddress.objects.filter(ipaddress='10.0.0.1').count(), 2)


class ModelTxtTestCase(TestCase):
    """This class defines the test suite for the Txt model."""

    def setUp(self):
        """Define the test client and other test variables."""
        # Needs sample host to test properly
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org',
                             ttl=300,
                             loc='23 58 23 N 10 43 50 E 80m',
                             comment='some comment')

        clean_and_save(self.host_one)

        self.txt_sample = Txt(host=Host.objects.get(name='some-host.example.org'),
                              txt='some-text')

    def test_model_can_create_txt(self):
        """Test that the model is able to create a txt entry."""
        old_count = Txt.objects.count()
        clean_and_save(self.txt_sample)
        new_count = Txt.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_txt(self):
        """Test that the model is able to change a txt entry."""
        clean_and_save(self.txt_sample)
        new_txt = 'some-new-text'
        txt_sample_id = self.txt_sample.id
        self.txt_sample.txt = new_txt
        clean_and_save(self.txt_sample)
        updated_txt = Txt.objects.get(pk=txt_sample_id).txt
        self.assertEqual(new_txt, updated_txt)

    def test_model_can_delete_txt(self):
        """Test that the model is able to delete a txt entry."""
        clean_and_save(self.txt_sample)
        old_count = Txt.objects.count()
        self.txt_sample.delete()
        new_count = Txt.objects.count()
        self.assertNotEqual(old_count, new_count)


class ModelCnameTestCase(TestCase):
    """This class defines the test suite for the Cname model."""

    def setUp(self):
        """Define the test client and other test variables."""
        # Needs sample host to test properly
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org')

        clean_and_save(self.host_one)

        self.cname_sample = Cname(host=Host.objects.get(name='some-host.example.org'),
                                  name='some-cname.example.org',
                                  ttl=300)

    def test_model_can_create_cname(self):
        """Test that the model is able to create a cname entry."""
        old_count = Cname.objects.count()
        clean_and_save(self.cname_sample)
        new_count = Cname.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_cname(self):
        """Test that the model is able to change a cname entry."""
        clean_and_save(self.cname_sample)
        new_cname = 'some-new-cname.example.org'
        self.cname_sample.name = new_cname
        clean_and_save(self.cname_sample)
        updated_cname = Cname.objects.filter(host__name='some-host.example.org')[0].name
        self.assertEqual(new_cname, updated_cname)

    def test_model_can_delete_cname(self):
        """Test that the model is able to delete a cname entry."""
        clean_and_save(self.cname_sample)
        old_count = Cname.objects.count()
        self.cname_sample.delete()
        new_count = Cname.objects.count()
        self.assertNotEqual(old_count, new_count)


class ModelNaptrTestCase(TestCase):
    """This class defines the test suite for the Naptr model."""

    def setUp(self):
        """Define the test client and other test variables."""
        # Needs sample host to test properly
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org',
                             ttl=300,
                             loc='23 58 23 N 10 43 50 E 80m',
                             comment='some comment')

        clean_and_save(self.host_one)

        self.naptr_sample = Naptr(host=Host.objects.get(name='some-host.example.org'),
                                  preference=1,
                                  order=1,
                                  flag='a',
                                  service='SER+VICE',
                                  regex='^naptrregex',
                                  replacement='some replacement')

    def test_model_can_create_naptr(self):
        """Test that the model is able to create a naptr entry."""
        old_count = Naptr.objects.count()
        clean_and_save(self.naptr_sample)
        new_count = Naptr.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_naptr(self):
        """Test that the model is able to change a naptr entry."""
        clean_and_save(self.naptr_sample)
        new_flag = 'u'
        self.naptr_sample.flag = new_flag
        clean_and_save(self.naptr_sample)
        updated_flag = Naptr.objects.get(pk=self.naptr_sample.id).flag
        self.assertEqual(new_flag, updated_flag)

    def test_model_can_delete_naptr(self):
        """Test that the model is able to delete a naptr entry."""
        clean_and_save(self.naptr_sample)
        old_count = Naptr.objects.count()
        self.naptr_sample.delete()
        new_count = Naptr.objects.count()
        self.assertNotEqual(old_count, new_count)


class ModelSrvTestCase(TestCase):
    """This class defines the test suite for the Srv model."""

    def setUp(self):
        """Define the test client and other test variables."""
        # Needs sample host to test properly
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org',
                             ttl=300,
                             loc='23 58 23 N 10 43 50 E 80m',
                             comment='some comment')

        clean_and_save(self.host_one)

        self.srv_sample = Srv(name='_abc._udp.example.org',
                              priority=3,
                              weight=1,
                              port=5433,
                              ttl=300,
                              target='some-target')

    def test_model_can_create_srv(self):
        """Test that the model is able to create a srv entry."""
        old_count = Srv.objects.count()
        clean_and_save(self.srv_sample)
        new_count = Srv.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_change_srv(self):
        """Test that the model is able to change a srv entry."""
        clean_and_save(self.srv_sample)
        new_port = 5434
        self.srv_sample.port = new_port
        clean_and_save(self.srv_sample)
        updated_port = Srv.objects.get(pk=self.srv_sample.id).port
        self.assertEqual(new_port, updated_port)

    def test_model_can_delete_srv(self):
        """Test that the model is able to delete a srv entry."""
        clean_and_save(self.srv_sample)
        old_count = Srv.objects.count()
        self.srv_sample.delete()
        new_count = Srv.objects.count()
        self.assertNotEqual(old_count, new_count)


class ModelChangeLogTestCase(TestCase):
    """This class defines the test suite for the ModelChangeLog model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org',
                             ttl=300,
                             loc='23 58 23 N 10 43 50 E 80m',
                             comment='some comment')
        clean_and_save(self.host_one)

        self.log_data = {'id': self.host_one.id,
                         'name': self.host_one.name,
                         'contact': self.host_one.contact,
                         'ttl': self.host_one.ttl,
                         'loc': self.host_one.loc,
                         'comment': self.host_one.comment}

        self.log_entry_one = ModelChangeLog(table_name='Hosts',
                                            table_row=self.host_one.id,
                                            data=self.log_data,
                                            action='saved',
                                            timestamp=timezone.now())

    def test_model_can_create_a_log_entry(self):
        """Test that the model is able to create a host."""
        old_count = ModelChangeLog.objects.count()
        clean_and_save(self.log_entry_one)
        new_count = ModelChangeLog.objects.count()
        self.assertNotEqual(old_count, new_count)


def get_token_client():
    user, created = User.objects.get_or_create(username='nobody')
    token, created = Token.objects.get_or_create(user=user)
    REQUIRED_USER_GROUP = getattr(settings, 'REQUIRED_USER_GROUP', None)
    if REQUIRED_USER_GROUP is not None:
        group, created = Group.objects.get_or_create(name=REQUIRED_USER_GROUP)
        group.user_set.add(user)
        group.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client

class APITokenAutheticationTestCase(APITestCase):
    """Test various token authentication operations."""

    def setUp(self):
        self.client = get_token_client()

    def test_logout(self):
        ret = self.client.get("/zones/")
        self.assertEqual(ret.status_code, 200)
        ret = self.client.post("/api/token-logout/")
        self.assertEqual(ret.status_code, 200)
        ret = self.client.get("/zones/")
        self.assertEqual(ret.status_code, 401)

    def test_force_expire(self):
        ret = self.client.get("/zones/")
        self.assertEqual(ret.status_code, 200)
        user = User.objects.get(username='nobody')
        token = Token.objects.get(user=user)
        EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 8)
        token.created = timezone.now() - timedelta(hours=EXPIRE_HOURS)
        token.save()
        ret = self.client.get("/zones/")
        self.assertEqual(ret.status_code, 401)



class APIAutoupdateZonesTestCase(APITestCase):
    """This class tests the autoupdate of zones' updated_at whenever
       various models are added/deleted/renamed/changed etc."""

    def setUp(self):
        """Add the a couple of zones and hosts for used in testing."""
        self.client = get_token_client()
        self.host1 = {"name": "host1.example.org",
                      "ipaddress": "10.10.0.1",
                      "contact": "mail@example.org"}
        self.delegation = {"name": "delegated.example.org",
                           "nameservers": "ns.example.org"}
        self.subzone = {"name": "sub.example.org",
                        "email": "hostmaster@example.org",
                        "primary_ns": "ns.example.org"}
        self.zone_exampleorg = ForwardZone(name='example.org',
                                           primary_ns='ns.example.org',
                                           email='hostmaster@example.org')
        self.zone_examplecom = ForwardZone(name='example.com',
                                           primary_ns='ns.example.com',
                                           email='hostmaster@example.com')
        self.zone_1010 = ReverseZone(name='10.10.in-addr.arpa',
                                     primary_ns='ns.example.org',
                                     email='hostmaster@example.org')
        clean_and_save(self.zone_exampleorg)
        clean_and_save(self.zone_examplecom)
        clean_and_save(self.zone_1010)

    def test_add_host(self):
        old_org_updated_at = self.zone_exampleorg.updated_at
        old_1010_updated_at = self.zone_1010.updated_at
        self.client.post('/hosts/', self.host1)
        self.zone_exampleorg.refresh_from_db()
        self.zone_1010.refresh_from_db()
        self.assertTrue(self.zone_exampleorg.updated)
        self.assertTrue(self.zone_1010.updated)
        self.assertGreater(self.zone_exampleorg.updated_at, old_org_updated_at)
        self.assertGreater(self.zone_1010.updated_at, old_1010_updated_at)

    def test_rename_host(self):
        self.client.post('/hosts/', self.host1)
        self.zone_exampleorg.refresh_from_db()
        self.zone_examplecom.refresh_from_db()
        self.zone_1010.refresh_from_db()
        old_org_updated_at = self.zone_exampleorg.updated_at
        old_com_updated_at = self.zone_examplecom.updated_at
        old_1010_updated_at = self.zone_1010.updated_at
        self.client.patch('/hosts/host1.example.org',
                          {"name": "host1.example.com"})
        self.zone_exampleorg.refresh_from_db()
        self.zone_examplecom.refresh_from_db()
        self.zone_1010.refresh_from_db()
        self.assertTrue(self.zone_examplecom.updated)
        self.assertTrue(self.zone_exampleorg.updated)
        self.assertTrue(self.zone_1010.updated)
        self.assertGreater(self.zone_examplecom.updated_at, old_com_updated_at)
        self.assertGreater(self.zone_exampleorg.updated_at, old_org_updated_at)
        self.assertGreater(self.zone_1010.updated_at, old_1010_updated_at)

    def test_change_soa(self):
        self.zone_exampleorg.updated = False
        self.zone_exampleorg.save()
        ret = self.client.patch('/zones/example.org', {'ttl': 1000})
        self.assertEqual(ret.status_code, 204)
        self.zone_exampleorg.refresh_from_db()
        self.assertTrue(self.zone_exampleorg.updated)

    def test_changed_nameservers(self):
        self.zone_exampleorg.updated = False
        self.zone_exampleorg.save()
        ret = self.client.patch('/zones/example.org/nameservers',
                                {'primary_ns': 'ns2.example.org'})
        self.assertEqual(ret.status_code, 204)
        self.zone_exampleorg.refresh_from_db()
        self.assertTrue(self.zone_exampleorg.updated)

    def test_added_subzone(self):
        self.zone_exampleorg.updated = False
        self.zone_exampleorg.save()
        self.client.post("/zones/", self.subzone)
        self.zone_exampleorg.refresh_from_db()
        self.assertTrue(self.zone_exampleorg.updated)

    def test_removed_subzone(self):
        self.client.post("/zones/", self.subzone)
        self.zone_exampleorg.updated = False
        self.zone_exampleorg.save()
        self.client.delete("/zones/sub.example.org")
        self.zone_exampleorg.refresh_from_db()
        self.assertTrue(self.zone_exampleorg.updated)

    def test_add_delegation(self):
        self.zone_exampleorg.updated = False
        self.zone_exampleorg.save()
        ret = self.client.post("/zones/example.org/delegations/", self.delegation)
        self.assertEqual(ret.status_code, 201)
        self.zone_exampleorg.refresh_from_db()
        self.assertTrue(self.zone_exampleorg.updated)

    def test_remove_delegation(self):
        self.client.post("/zones/example.org/delegations/", self.delegation)
        self.zone_exampleorg.updated = False
        self.zone_exampleorg.save()
        self.client.delete("/zones/example.org/delegations/delegated.example.org")
        self.zone_exampleorg.refresh_from_db()
        self.assertTrue(self.zone_exampleorg.updated)


class APIAutoupdateHostZoneTestCase(APITestCase):
    """This class tests that a Host's zone attribute is correct and updated
       when renaming etc.
       """

    def setUp(self):
        """Add the a couple of zones and hosts for used in testing."""
        self.client = get_token_client()
        self.zone_org = ForwardZone(name='example.org',
                                    primary_ns='ns.example.org',
                                    email='hostmaster@example.org')
        self.zone_long = ForwardZone(name='longexample.org',
                                     primary_ns='ns.example.org',
                                     email='hostmaster@example.org')
        self.zone_sub = ForwardZone(name='sub.example.org',
                                    primary_ns='ns.example.org',
                                    email='hostmaster@example.org')
        self.zone_com = ForwardZone(name='example.com',
                                    primary_ns='ns.example.com',
                                    email='hostmaster@example.com')
        self.zone_1010 = ReverseZone(name='10.10.in-addr.arpa',
                                     primary_ns='ns.example.org',
                                     email='hostmaster@example.org')

        self.org_host1 = {"name": "host1.example.org",
                         "ipaddress": "10.10.0.1",
                         "contact": "mail@example.org"}
        self.org_host2 = {"name": "example.org",
                          "ipaddress": "10.10.0.2",
                          "contact": "mail@example.org"}
        self.sub_host1 = {"name": "host1.sub.example.org",
                          "ipaddress": "10.20.0.1",
                          "contact": "mail@example.org"}
        self.sub_host2 = {"name": "sub.example.org",
                          "ipaddress": "10.20.0.1",
                          "contact": "mail@example.org"}
        self.long_host1 = {"name": "host1.longexample.org",
                           "ipaddress": "10.30.0.1",
                           "contact": "mail@example.org"}
        self.long_host2 = {"name": "longexample.org",
                           "ipaddress": "10.30.0.2",
                           "contact": "mail@example.org"}
        clean_and_save(self.zone_org)
        clean_and_save(self.zone_long)
        clean_and_save(self.zone_com)
        clean_and_save(self.zone_sub)
        clean_and_save(self.zone_1010)

    def test_add_host_known_zone(self):
        res = self.client.post("/hosts/", self.org_host1)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/hosts/", self.org_host2)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/hosts/", self.sub_host1)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/hosts/", self.sub_host2)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/hosts/", self.long_host1)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/hosts/", self.long_host2)
        self.assertEqual(res.status_code, 201)

        res =  self.client.get("/hosts/{}".format(self.org_host1['name']))
        self.assertEqual(res.json()['zone'], self.zone_org.id)
        res =  self.client.get("/hosts/{}".format(self.org_host2['name']))
        self.assertEqual(res.json()['zone'], self.zone_org.id)
        res =  self.client.get("/hosts/{}".format(self.sub_host1['name']))
        self.assertEqual(res.json()['zone'], self.zone_sub.id)
        res =  self.client.get("/hosts/{}".format(self.sub_host2['name']))
        self.assertEqual(res.json()['zone'], self.zone_sub.id)
        res =  self.client.get("/hosts/{}".format(self.long_host1['name']))
        self.assertEqual(res.json()['zone'], self.zone_long.id)
        res =  self.client.get("/hosts/{}".format(self.long_host2['name']))
        self.assertEqual(res.json()['zone'], self.zone_long.id)

    def test_add_to_non_existant(self):
        data = {"name": "host1.example.net",
                "ipaddress": "10.10.0.10",
                "contact": "mail@example.org"}
        res = self.client.post("/hosts/", data)
        self.assertEqual(res.status_code, 201)
        res = self.client.get(f"/hosts/{data['name']}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['zone'], None)


    def test_rename_host_to_valid_zone(self):
        self.client.post('/hosts/', self.org_host1)
        self.client.patch('/hosts/host1.example.org',
                          {"name": "host1.example.com"})
        res = self.client.get(f"/hosts/host1.example.com")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['zone'], self.zone_com.id)

    def test_rename_host_to_unknown_zone(self):
        self.client.post('/hosts/', self.org_host1)
        self.client.patch('/hosts/host1.example.org',
                          {"name": "host1.example.net"})
        res = self.client.get(f"/hosts/host1.example.net")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['zone'], None)


class APIHostsTestCase(TestCase):
    """This class defines the test suite for api/hosts"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.host_one = Host(name='host1.example.org', contact='mail1@example.org')
        self.host_two = Host(name='host2.example.org', contact='mail2@example.org')
        self.patch_data = {'name': 'new-name1.example.com', 'contact': 'updated@mail.com'}
        self.patch_data_name = {'name': 'host2.example.org', 'contact': 'updated@mail.com'}
        self.post_data = {'name': 'new-name2.example.org', "ipaddress": '127.0.0.2',
                          'contact': 'hostmaster@example.org'}
        self.post_data_name = {'name': 'host1.example.org', "ipaddress": '127.0.0.2',
                               'contact': 'hostmaster@example.org'}
        self.zone_sample = ForwardZone(name='example.org',
                                       primary_ns='ns.example.org',
                                       email='hostmaster@example.org')
        clean_and_save(self.host_one)
        clean_and_save(self.host_two)
        clean_and_save(self.zone_sample)
        self.client = get_token_client()

    def test_hosts_get_200_ok(self):
        """"Getting an existing entry should return 200"""
        response = self.client.get('/hosts/%s' % self.host_one.name)
        self.assertEqual(response.status_code, 200)

    def test_hosts_list_200_ok(self):
        """List all hosts should return 200"""
        response = self.client.get('/hosts/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)

    def test_hosts_get_404_not_found(self):
        """"Getting a non-existing entry should return 404"""
        response = self.client.get('/hosts/nonexistent.example.org')
        self.assertEqual(response.status_code, 404)

    def test_hosts_post_201_created(self):
        """"Posting a new host should return 201 and location"""
        response = self.client.post('/hosts/', self.post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], '/hosts/%s' % self.post_data['name'])

    def test_hosts_post_400_invalid_ip(self):
        """"Posting a new host with an invalid IP should return 400"""
        post_data = {'name': 'failing.example.org', 'ipaddress': '300.400.500.600',
                     'contact': 'fail@example.org'}
        response = self.client.post('/hosts/', post_data)
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/hosts/failing.example.org')
        self.assertEqual(response.status_code, 404)


    def test_hosts_post_409_conflict_name(self):
        """"Posting a new host with a name already in use should return 409"""
        response = self.client.post('/hosts/', self.post_data_name)
        self.assertEqual(response.status_code, 409)

    def test_hosts_patch_204_no_content(self):
        """Patching an existing and valid entry should return 204 and Location"""
        response = self.client.patch('/hosts/%s' % self.host_one.name, self.patch_data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['Location'], '/hosts/%s' % self.patch_data['name'])

    def test_hosts_patch_without_name_204_no_content(self):
        """Patching an existing entry without having name in patch should
        return 204"""
        response = self.client.patch('/hosts/%s' % self.host_one.name, {"ttl": 5000})
        self.assertEqual(response.status_code, 204)

    def test_hosts_patch_400_bad_request(self):
        """Patching with invalid data should return 400"""
        response = self.client.patch('/hosts/%s' % self.host_one.name, data={'this': 'is', 'so': 'wrong'})
        self.assertEqual(response.status_code, 400)

    def test_hosts_patch_400_bad_ttl(self):
        """Patching with invalid ttl should return 400"""
        response = self.client.patch('/hosts/%s' % self.host_one.name, data={'ttl': 100})
        self.assertEqual(response.status_code, 400)

    def test_hosts_patch_404_not_found(self):
        """Patching a non-existing entry should return 404"""
        response = self.client.patch('/hosts/feil-navn/', self.patch_data)
        self.assertEqual(response.status_code, 404)

    def test_hosts_patch_409_conflict_name(self):
        """Patching an entry with a name that already exists should return 409"""
        response = self.client.patch('/hosts/%s' % self.host_one.name, {'name': self.host_two.name})
        self.assertEqual(response.status_code, 409)


class APIMxTestcase(APITestCase):
    """Test MX records."""

    def setUp(self):
        self.client = get_token_client()
        self.zone = ForwardZone(name='example.org',
                                primary_ns='ns1.example.org',
                                email='hostmaster@example.org')
        clean_and_save(self.zone)
        self.host_data = {'name': 'ns1.example.org',
                          'contact': 'mail@example.org'}
        self.client.post('/hosts/', self.host_data)
        self.host = Host.objects.get(name=self.host_data['name'])

    def test_mx_post(self):
        data = {'host': self.host.id,
                'priority': 10,
                'mx': 'smtp.example.org'}
        ret = self.client.post("/mxs/", data)
        self.assertEqual(ret.status_code, 201)

    def test_mx_post_reject_invalid(self):
        # priority is an 16 bit uint, e.g. 0..65535.
        data = {'host': self.host.id,
                'priority': -1,
                'mx': 'smtp.example.org'}
        ret = self.client.post("/mxs/", data)
        self.assertEqual(ret.status_code, 400)
        data = {'host': self.host.id,
                'priority': 1000000,
                'mx': 'smtp.example.org'}
        ret = self.client.post("/mxs/", data)
        self.assertEqual(ret.status_code, 400)
        data = {'host': self.host.id,
                'priority': 1000,
                'mx': 'invalidhostname'}
        ret = self.client.post("/mxs/", data)
        self.assertEqual(ret.status_code, 400)

    def test_mx_list(self):
        self.test_mx_post()
        ret = self.client.get("/mxs/")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.data['count'], 1)

    def test_mx_delete(self):
        self.test_mx_post()
        mxs = self.client.get("/mxs/").json()['results']
        ret = self.client.delete("/mxs/{}".format(mxs[0]['id']))
        self.assertEqual(ret.status_code, 204)
        mxs = self.client.get("/mxs/").json()
        self.assertEqual(len(mxs['results']), 0)

    def test_mx_zone_autoupdate_add(self):
        self.zone.updated = False
        self.zone.save()
        self.test_mx_post()
        self.zone.refresh_from_db()
        self.assertTrue(self.zone.updated)

    def test_mx_zone_autoupdate_delete(self):
        self.test_mx_post()
        self.zone.updated = False
        self.zone.save()
        mxs = self.client.get("/mxs/").data['results']
        self.client.delete("/mxs/{}".format(mxs[0]['id']))
        self.zone.refresh_from_db()
        self.assertTrue(self.zone.updated)


class APIForwardZonesTestCase(APITestCase):
    """"This class defines the test suite for forward zones API """

    def setUp(self):
        """Define the test client and other variables."""
        self.client = get_token_client()
        self.zone_one = ForwardZone(
            name="example.org",
            primary_ns="ns1.example.org",
            email="hostmaster@example.org")
        self.host_one = Host(name='ns1.example.org', contact="hostmaster@example.org")
        self.host_two = Host(name='ns2.example.org', contact="hostmaster@example.org")
        self.host_three = Host(name='ns3.example.org', contact="hostmaster@example.org")
        self.ns_one = NameServer(name='ns1.example.org', ttl=400)
        self.ns_two = NameServer(name='ns2.example.org', ttl=400)
        self.post_data_one = {'name': 'example.com',
                              'primary_ns': ['ns1.example.org', 'ns2.example.org'],
                              'email': "hostmaster@example.org",
                              'refresh': 400, 'retry': 300, 'expire': 800, 'ttl': 350}
        self.post_data_two = {'name': 'example.net',
                              'primary_ns': ['ns1.example.org', 'ns2.example.org'],
                              'email': "hostmaster@example.org"}
        self.patch_data = {'refresh': '500', 'expire': '1000'}
        clean_and_save(self.host_one)
        clean_and_save(self.host_two)
        clean_and_save(self.ns_one)
        clean_and_save(self.ns_two)
        clean_and_save(self.zone_one)

    def test_zones_get_404_not_found(self):
        """"Getting a non-existing entry should return 404"""
        response = self.client.get('/zones/nonexisting.example.org')
        self.assertEqual(response.status_code, 404)

    def test_zones_get_200_ok(self):
        """"Getting an existing entry should return 200"""
        response = self.client.get('/zones/%s' % self.zone_one.name)
        self.assertEqual(response.status_code, 200)

    def test_zones_list_200_ok(self):
        """Listing all zones should return 200"""
        response = self.client.get('/zones/')
        self.assertEqual(response.json()[0]['name'], self.zone_one.name)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)

    def test_zones_post_409_name_conflict(self):
        """"Posting a entry that uses a name that is already taken should return 409"""
        response = self.client.get('/zones/%s' % self.zone_one.name)
        response = self.client.post('/zones/', {'name': response.data['name']})
        self.assertEqual(response.status_code, 409)

    def test_zones_post_201_created(self):
        """"Posting a new zone should return 201 and location"""
        response = self.client.post('/zones/', self.post_data_one)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], '/zones/%s' % self.post_data_one['name'])

    def test_zones_post_serialno(self):
        """serialno should be based on the current date and a sequential number"""
        self.client.post('/zones/', self.post_data_one)
        self.client.post('/zones/', self.post_data_two)
        response_one = self.client.get('/zones/%s' % self.post_data_one['name'])
        response_two = self.client.get('/zones/%s' % self.post_data_two['name'])
        self.assertEqual(response_one.data['serialno'], response_two.data['serialno'])
        self.assertEqual(response_one.data['serialno'], create_serialno())

    def test_zones_patch_403_forbidden_name(self):
        """"Trying to patch the name of an entry should return 403"""
        response = self.client.get('/zones/%s' % self.zone_one.name)
        response = self.client.patch('/zones/%s' % self.zone_one.name, {'name': response.data['name']})
        self.assertEqual(response.status_code, 403)

    def test_zones_patch_403_forbidden_primary_ns(self):
        """Trying to patch the primary_ns to be a nameserver that isn't in the nameservers list should return 403"""
        response = self.client.post('/zones/', self.post_data_two)
        self.assertEqual(response.status_code, 201)
        response = self.client.patch('/zones/%s' % self.post_data_two['name'], {'primary_ns': self.host_three.name})
        self.assertEqual(response.status_code, 403)

    def test_zones_patch_404_not_found(self):
        """"Patching a non-existing entry should return 404"""
        response = self.client.patch("/zones/nonexisting.example.org", self.patch_data)
        self.assertEqual(response.status_code, 404)

    def test_zones_patch_204_no_content(self):
        """"Patching an existing entry with valid data should return 204"""
        response = self.client.patch('/zones/%s' % self.zone_one.name, self.patch_data)
        self.assertEqual(response.status_code, 204)

    def test_zones_delete_204_no_content(self):
        """"Deleting an existing entry with no conflicts should return 204"""
        response = self.client.delete('/zones/%s' % self.zone_one.name)
        self.assertEqual(response.status_code, 204)

    def test_zones_404_not_found(self):
        """"Deleting a non-existing entry should return 404"""
        response = self.client.delete("/zones/nonexisting.example.org")
        self.assertEqual(response.status_code, 404)

    def test_zones_403_forbidden(self):
        # TODO: jobb skal gjøres her
        """"Deleting an entry with registered entries should require force"""


class APIZonesForwardDelegationTestCase(APITestCase):
    """ This class defines test testsuite for api/zones/<name>/delegations/
        But only for ForwardZones.
    """

    def setUp(self):
        """Define the test client and other variables."""
        self.client = get_token_client()
        self.data_exampleorg = {'name': 'example.org',
                                'primary_ns': ['ns1.example.org', 'ns2.example.org'],
                                'email': "hostmaster@example.org"}
        self.client.post("/zones/", self.data_exampleorg)

    def test_list_empty_delegation_200_ok(self):
        response = self.client.get(f"/zones/example.org/delegations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_delegate_forward_201_ok(self):
        path = "/zones/example.org/delegations/"
        data = {'name': 'delegated.example.org',
                'nameservers': ['ns1.example.org', 'ns1.delegated.example.org']}
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], f"{path}delegated.example.org")

    def test_delegate_forward_zonefiles_200_ok(self):
        self.test_delegate_forward_201_ok()
        response = self.client.get('/zonefiles/example.org')
        self.assertEqual(response.status_code, 200)

    def test_delegate_forward_badname_400_bad_request(self):
        path = "/zones/example.org/delegations/"
        bad = {'name': 'delegated.example.com',
               'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)

    def test_delegate_forward_no_ns_400_bad_request(self):
        path = "/zones/example.org/delegations/"
        bad = {'name': 'delegated.example.org',
               'nameservers': []}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)
        bad = {'name': 'delegated.example.org' }
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)

    def test_delegate_forward_duplicate_ns_400_bad_request(self):
        path = "/zones/example.org/delegations/"
        bad = {'name': 'delegated.example.org',
               'nameservers': ['ns1.example.org', 'ns1.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)

    def test_delegate_forward_invalid_ns_400_bad_request(self):
        path = "/zones/example.org/delegations/"
        bad = {'name': 'delegated.example.org',
               'nameservers': ['ns1', ]}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)
        bad = {'name': 'delegated.example.org',
               'nameservers': ['2"#¤2342.tld', ]}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)

    def test_delegate_forward_nameservers_list_200_ok(self):
        path = "/zones/example.org/delegations/"
        self.test_delegate_forward_201_ok()
        response = self.client.get(f"{path}delegated.example.org")
        self.assertEqual(response.status_code, 200)
        nameservers = [i['name'] for i in response.json()['nameservers']]
        self.assertEqual(len(nameservers), 2)
        for ns in nameservers:
            self.assertTrue(NameServer.objects.filter(name=ns).exists())

    def test_forward_list_delegations_200_ok(self):
        path = "/zones/example.org/delegations/"
        self.test_delegate_forward_201_ok()
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]['name'], 'delegated.example.org')

    def test_forward_delete_delegattion_204_ok(self):
        self.test_forward_list_delegations_200_ok()
        path = "/zones/example.org/delegations/delegated.example.org"
        self.assertEqual(NameServer.objects.count(), 3)
        response = self.client.delete(path)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['Location'], path)
        self.assertEqual(NameServer.objects.count(), 2)
        path = "/zones/example.org/delegations/"
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])


class APIZonesReverseDelegationTestCase(APITestCase):
    """ This class defines test testsuite for api/zones/<name>/delegations/
        But only for ReverseZones.
    """

    def setUp(self):
        """Define the test client and other variables."""
        self.client = get_token_client()
        self.data_rev1010 = {'name': '10.10.in-addr.arpa',
                             'primary_ns': ['ns1.example.org', 'ns2.example.org'],
                             'email': "hostmaster@example.org"}
        self.data_revdb8 = {'name': '8.b.d.0.1.0.0.2.ip6.arpa',
                            'primary_ns': ['ns1.example.org', 'ns2.example.org'],
                            'email': "hostmaster@example.org"}

        self.del_101010 = {'name': '10.10.10.in-addr.arpa',
                           'nameservers': ['ns1.example.org', 'ns2.example.org']}
        self.del_10101010 = {'name': '10.10.10.10.in-addr.arpa',
                             'nameservers': ['ns1.example.org', 'ns2.example.org']}
        self.del_2001db810 = {'name': '0.1.0.0.8.b.d.0.1.0.0.2.ip6.arpa',
                              'nameservers': ['ns1.example.org', 'ns2.example.org']}

        self.client.post("/zones/", self.data_rev1010)
        self.client.post("/zones/", self.data_revdb8)

    def test_get_delegation_200_ok(self):
        def assertempty(data):
            response = self.client.get(f"/zones/{data['name']}/delegations/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['count'], 0)
            self.assertEqual(response.data['results'], [])
        for data in ('rev1010', 'revdb8'):
            assertempty(getattr(self, f"data_{data}"))

    def test_delegate_ipv4_201_ok(self):
        path = "/zones/10.10.in-addr.arpa/delegations/"
        response = self.client.post(path, self.del_101010)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], f"{path}10.10.10.in-addr.arpa")
        response = self.client.post(path, self.del_10101010)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], f"{path}10.10.10.10.in-addr.arpa")

    def test_delegate_ipv4_zonefiles_200_ok(self):
        self.test_delegate_ipv4_201_ok()
        response = self.client.get('/zonefiles/10.10.in-addr.arpa')
        self.assertEqual(response.status_code, 200)

    def test_delegate_ipv4_badname_400_bad_request(self):
        path = "/zones/10.10.in-addr.arpa/delegations/"
        bad = {'name': 'delegated.example.com',
               'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)

    def test_delegate_ipv4_invalid_zone_400_bad_request(self):
        path = "/zones/10.10.in-addr.arpa/delegations/"
        bad = {'name': '300.10.10.in-addr.arpa',
               'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)
        bad = {'name': '10.10.10.10.10.in-addr.arpa',
               'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)
        bad = {'name': 'foo.10.10.in-addr.arpa',
               'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)

    def test_delegate_ipv4_wrong_inet_400_bad_request(self):
        path = "/zones/10.10.in-addr.arpa/delegations/"
        bad = {'name': '0.0.0.0.0.1.0.0.8.b.d.0.1.0.0.2.ip6.arpa',
               'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)

    def test_delegate_duplicate_409_conflict(self):
        path = "/zones/10.10.in-addr.arpa/delegations/"
        response = self.client.post(path, self.del_101010)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(path, self.del_101010)
        self.assertEqual(response.status_code, 409)

    def test_delegate_ipv6_201_ok(self):
        path = "/zones/8.b.d.0.1.0.0.2.ip6.arpa/delegations/"
        response = self.client.post(path, self.del_2001db810)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], f"{path}{self.del_2001db810['name']}")

    def test_delegate_ipv6_zonefiles_200_ok(self):
        self.test_delegate_ipv6_201_ok()
        response = self.client.get('/zonefiles/8.b.d.0.1.0.0.2.ip6.arpa')
        self.assertEqual(response.status_code, 200)

    def test_delegate_ipv6_badname_400_bad_request(self):
        path = "/zones/8.b.d.0.1.0.0.2.ip6.arpa/delegations/"
        bad = {'name': 'delegated.example.com',
               'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)

    def test_delegate_ipv6_wrong_inet_400_bad_request(self):
        path = "/zones/8.b.d.0.1.0.0.2.ip6.arpa/delegations/"
        bad = {'name': '10.10.in-addr.arpa',
               'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post(path, bad)
        self.assertEqual(response.status_code, 400)


class APIZonesNsTestCase(APITestCase):
    """"This class defines the test suite for api/zones/<name>/nameservers/ """

    def setUp(self):
        """Define the test client and other variables."""
        self.client = get_token_client()
        self.post_data = {'name': 'example.org', 'primary_ns': ['ns2.example.org'],
                          'email': "hostmaster@example.org"}
        self.ns_one = Host(name='ns1.example.org', contact='mail@example.org')
        self.ns_two = Host(name='ns2.example.org', contact='mail@example.org')
        clean_and_save(self.ns_one)
        clean_and_save(self.ns_two)

    def test_zones_ns_get_200_ok(self):
        """"Getting the list of nameservers of a existing zone should return 200"""
        self.assertEqual(NameServer.objects.count(), 0)
        self.client.post('/zones/', self.post_data)
        self.assertEqual(NameServer.objects.count(), 1)
        response = self.client.get('/zones/%s/nameservers' % self.post_data['name'])
        self.assertEqual(response.status_code, 200)

    def test_zones_ns_get_404_not_found(self):
        """"Getting the list of nameservers of a non-existing zone should return 404"""
        response = self.client.delete('/zones/example.com/nameservers/')
        self.assertEqual(response.status_code, 404)

    def test_zones_ns_patch_204_no_content(self):
        """"Patching the list of nameservers with an existing nameserver should return 204"""
        self.client.post('/zones/', self.post_data)
        response = self.client.patch('/zones/%s/nameservers' % self.post_data['name'],
                                     {'primary_ns': self.post_data['primary_ns'] + [self.ns_one.name]})
        self.assertEqual(response.status_code, 204)

    def test_zones_ns_patch_400_bad_request(self):
        """"Patching the list of nameservers with a bad request body should return 404"""
        self.client.post('/zones/', self.post_data)
        response = self.client.patch('/zones/%s/nameservers' % self.post_data['name'],
                                     {'garbage': self.ns_one.name})
        self.assertEqual(response.status_code, 400)

    def test_zones_ns_patch_404_not_found(self):
        """"Patching the list of nameservers with a non-existing nameserver should return 404"""
        self.client.post('/zones/', self.post_data)
        response = self.client.patch('/zones/%s/nameservers' % self.post_data['name'],
                                     {'primary_ns': ['nonexisting-ns.example.org']})
        # XXX: This is now valid, as the NS might point to a server in a zone which we
        # don't control. Might be possible to check if the attempted NS is in a
        # zone we control and then be stricter.
        return
        self.assertEqual(response.status_code, 404)

    def test_zones_ns_delete_204_no_content_zone(self):
        """Deleting a nameserver from an existing zone should return 204"""
        self.assertFalse(NameServer.objects.exists())
        # TODO: This test needs some cleanup and work. See comments
        self.client.post('/zones/', self.post_data)

        response = self.client.patch('/zones/%s/nameservers' % self.post_data['name'],
                                     {'primary_ns': self.post_data['primary_ns'] + [self.ns_one.name]})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(NameServer.objects.count(), 2)

        response = self.client.get('/zones/%s/nameservers' % self.post_data['name'])
        self.assertEqual(response.status_code, 200)

        response = self.client.patch('/zones/%s/nameservers' % self.post_data['name'],
                                     {'primary_ns': self.ns_two.name})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(NameServer.objects.count(), 1)

        response = self.client.get('/zones/%s/nameservers' % self.post_data['name'])
        self.assertEqual(response.data, self.post_data['primary_ns'])
        response = self.client.delete('/zones/%s' % self.post_data['name'])
        self.assertEqual(response.status_code, 204)
        self.assertFalse(NameServer.objects.exists())

class APIZoneRFC2317(APITestCase):
    """This class tests RFC 2317 delegations."""

    def setUp(self):
        self.client = get_token_client()
        self.data = {'name': '128/25.0.0.10.in-addr.arpa',
                     'primary_ns': ['ns1.example.org', 'ns2.example.org'],
                     'email': "hostmaster@example.org"}


    def test_create_and_get_rfc_2317_zone(self):
        # Create and get zone for 10.0.0.128/25
        response = self.client.post("/zones/", self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["location"], "/zones/128/25.0.0.10.in-addr.arpa")
        response = self.client.get(response["location"])
        self.assertEqual(response.status_code, 200)


    def test_add_rfc2317_delegation_for_existing_zone(self):
        zone = {'name': '0.10.in-addr.arpa',
                'primary_ns': ['ns1.example.org', 'ns2.example.org'],
                'email': "hostmaster@example.org"}
        response = self.client.post("/zones/", zone)
        self.assertEqual(response.status_code, 201)
        delegation = {'name': '128/25.0.0.10.in-addr.arpa',
                      'nameservers': ['ns1.example.org', 'ns2.example.org']}
        response = self.client.post("/zones/0.10.in-addr.arpa/delegations/", delegation)
        self.assertEqual(response.status_code, 201)


    def test_delete_rfc2317_zone(self):
        self.client.post("/zones/", self.data)
        response = self.client.delete("/zones/128/25.0.0.10.in-addr.arpa")
        self.assertEqual(response.status_code, 204)


class APIIPaddressesTestCase(APITestCase):
    """This class defines the test suite for api/ipaddresses"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = get_token_client()
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org')

        self.host_two = Host(name='some-other-host.example.org',
                             contact='mail@example.com')

        clean_and_save(self.host_one)
        clean_and_save(self.host_two)

        self.ipaddress_one = Ipaddress(host=self.host_one,
                                       ipaddress='129.240.111.111')

        self.ipaddress_two = Ipaddress(host=self.host_two,
                                       ipaddress='129.240.111.112')

        clean_and_save(self.ipaddress_one)
        clean_and_save(self.ipaddress_two)

        self.post_data_full = {'host': self.host_one.id,
                               'ipaddress': '129.240.203.197'}
        self.post_data_full_conflict = {'host': self.host_one.id,
                                        'ipaddress': self.ipaddress_one.ipaddress}
        self.post_data_full_duplicate_ip = {'host': self.host_two.id,
                                            'ipaddress': self.ipaddress_one.ipaddress}
        self.patch_data_ip = {'ipaddress': '129.240.203.198'}
        self.patch_bad_ip = {'ipaddress': '129.240.300.1'}

    def test_ipaddress_get_200_ok(self):
        """"Getting an existing entry should return 200"""
        response = self.client.get('/ipaddresses/%s' % self.ipaddress_one.id)
        self.assertEqual(response.status_code, 200)

    def test_ipaddress_list_200_ok(self):
        """List all ipaddress should return 200"""
        response = self.client.get('/ipaddresses/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)

    def test_ipaddress_get_404_not_found(self):
        """"Getting a non-existing entry should return 404"""
        response = self.client.get('/ipaddresses/193.101.168.2')
        self.assertEqual(response.status_code, 404)

    def test_ipaddress_post_201_created(self):
        """"Posting a new ip should return 201"""
        response = self.client.post('/ipaddresses/', self.post_data_full)
        self.assertEqual(response.status_code, 201)

    def test_ipaddress_post_400_conflict_ip(self):
        """"Posting an existing ip for a host should return 400"""
        response = self.client.post('/ipaddresses/', self.post_data_full_conflict)
        self.assertEqual(response.status_code, 400)

    def test_ipaddress_post_201_two_hosts_share_ip(self):
        """"Posting a new ipaddress with an ip already in use should return 201"""
        response = self.client.post('/ipaddresses/', self.post_data_full_duplicate_ip)
        self.assertEqual(response.status_code, 201)

    def test_ipaddress_patch_200_ok(self):
        """Patching an existing and valid entry should return 200"""
        response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id, self.patch_data_ip)
        self.assertEqual(response.status_code, 200)

    def test_ipaddress_patch_200_own_ip(self):
        """Patching an entry with its own ip should return 200"""
        response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id,
                                     {'ipaddress': str(self.ipaddress_one.ipaddress)})
        self.assertEqual(response.status_code, 200)

    def test_ipaddress_patch_400_bad_request(self):
        """Patching with invalid data should return 400"""
        response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id,
                                     data={'this': 'is', 'so': 'wrong'})
        self.assertEqual(response.status_code, 400)

    def test_ipaddress_patch_400_bad_ip(self):
        """Patching with invalid data should return 400"""
        response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id, self.patch_bad_ip)
        self.assertEqual(response.status_code, 400)

    def test_ipaddress_patch_404_not_found(self):
        """Patching a non-existing entry should return 404"""
        response = self.client.patch('/ipaddresses/1234567890', self.patch_data_ip)
        self.assertEqual(response.status_code, 404)


class APIMACaddressTestCase(APITestCase):
    """This class defines the test suite for api/ipaddresses with macadresses"""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = get_token_client()
        self.host_one = Host(name='host1.example.org',
                             contact='mail@example.org')

        self.host_two = Host(name='host2.example.org',
                             contact='mail@example.com')

        clean_and_save(self.host_one)
        clean_and_save(self.host_two)

        self.ipaddress_one = Ipaddress(host=self.host_one,
                                       ipaddress='10.0.0.10',
                                       macaddress='aa:bb:cc:00:00:10')

        self.ipaddress_two = Ipaddress(host=self.host_two,
                                       ipaddress='10.0.0.11',
                                       macaddress='aa:bb:cc:00:00:11')

        clean_and_save(self.ipaddress_one)
        clean_and_save(self.ipaddress_two)

        self.post_data_full = {'host': self.host_one.id,
                               'ipaddress': '10.0.0.12',
                               'macaddress': 'aa:bb:cc:00:00:12'}
        self.post_data_full_conflict = {'host': self.host_one.id,
                                        'ipaddress': self.ipaddress_one.ipaddress,
                                        'macaddress': self.ipaddress_one.macaddress}
        self.patch_mac = {'macaddress': 'aa:bb:cc:00:00:ff'}
        self.patch_mac_in_use = {'macaddress': self.ipaddress_two.macaddress}
        self.patch_ip_and_mac = {'ipaddress': '10.0.0.13',
                                 'macaddress': 'aa:bb:cc:00:00:ff'}

    def test_mac_post_ip_with_mac_201_ok(self):
        """Post a new IP with MAC should return 201 ok."""
        response = self.client.post('/ipaddresses/', self.post_data_full)
        self.assertEqual(response.status_code, 201)

    def test_mac_post_conflict_ip_and_mac_400_bad_request(self):
        """"Posting an existing IP and mac IP a host should return 400."""
        response = self.client.post('/ipaddresses/', self.post_data_full_conflict)
        self.assertEqual(response.status_code, 400)

    def test_mac_patch_mac_200_ok(self):
        """Patch an IP with a new mac should return 200 ok."""
        response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id,
                                    self.patch_mac)
        self.assertEqual(response.status_code, 200)

    def test_mac_remove_mac_200_ok(self):
        """Patch an IP to remove MAC should return 200 ok."""
        response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id,
                                     {'macaddress': ''})
        self.assertEqual(response.status_code, 200)

    def test_mac_patch_mac_in_use_400_bad_request(self):
        """Patch an IP with a MAC in use should return 400 bad request."""
        response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id,
                                    self.patch_mac_in_use)
        self.assertEqual(response.status_code, 400)

    def test_mac_patch_invalid_mac_400_bad_request(self):
        """ Patch an IP with invalid MAC should return 400 bad request."""
        for mac in ('00:00:00:00:00:XX', '00:00:00:00:00', 'AA:BB:cc:dd:ee:ff'):
            response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id,
                                         {'macaddress': mac})
            self.assertEqual(response.status_code, 400)

    def test_mac_patch_ip_and_mac_200_ok(self):
        """Patch an IP with a new IP and MAC should return 200 ok."""
        response = self.client.patch('/ipaddresses/%s' % self.ipaddress_one.id,
                                    self.patch_ip_and_mac)
        self.assertEqual(response.status_code, 200)

    def test_mac_with_network(self):
        self.network_one = Network(range='10.0.0.0/24')
        clean_and_save(self.network_one)
        self.test_mac_post_ip_with_mac_201_ok()
        self.test_mac_patch_ip_and_mac_200_ok()
        self.test_mac_patch_mac_200_ok()

    def test_mac_with_network_vlan(self):
        self.network_one = Network(range='10.0.0.0/24', vlan=10)
        self.network_two = Network(range='10.0.1.0/24', vlan=10)
        self.network_ipv6 = Network(range='2001:db8:1::/64', vlan=10)
        clean_and_save(self.network_one)
        clean_and_save(self.network_two)
        clean_and_save(self.network_ipv6)
        self.test_mac_post_ip_with_mac_201_ok()
        self.test_mac_patch_ip_and_mac_200_ok()
        self.test_mac_patch_mac_200_ok()
        # Make sure it is allowed to add a mac to both IPv4 and IPv6
        # addresses on the same vlan
        response = self.client.post('/ipaddresses/',
                                    {'host': self.host_one.id,
                                     'ipaddress': '10.0.1.10',
                                     'macaddress': '11:22:33:44:55:66'})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/ipaddresses/',
                                    {'host': self.host_one.id,
                                     'ipaddress': '2001:db8:1::10',
                                     'macaddress': '11:22:33:44:55:66'})
        self.assertEqual(response.status_code, 201)


class APICnamesTestCase(APITestCase):
    """This class defines the test suite for api/cnames """
    def setUp(self):
        self.client = get_token_client()
        self.zone_one = ForwardZone(name='example.org',
                                    primary_ns='ns.example.org',
                                    email='hostmaster@example.org')
        self.zone_two = ForwardZone(name='example.net',
                                    primary_ns='ns.example.net',
                                    email='hostmaster@example.org')
        clean_and_save(self.zone_one)
        clean_and_save(self.zone_two)

        self.post_host_one = {'name': 'host1.example.org',
                              'contact': 'mail@example.org' }
        self.client.post('/hosts/', self.post_host_one)
        self.host_one = self.client.get('/hosts/%s' % self.post_host_one['name']).data
        self.post_host_two = {'name': 'host2.example.org',
                              'contact': 'mail@example.org' }
        self.client.post('/hosts/', self.post_host_two)
        self.host_two = self.client.get('/hosts/%s' % self.post_host_two['name']).data

        self.post_data = {'name': 'host-alias.example.org',
                          'host': self.host_one['id'],
                          'ttl': 5000 }

    def test_cname_post_201_ok(self):
        """ Posting a cname should return 201 OK"""
        response = self.client.post('/cnames/', self.post_data)
        self.assertEqual(response.status_code, 201)

    def test_cname_get_200_ok(self):
        """GET on an existing cname should return 200 OK."""
        self.client.post('/cnames/', self.post_data)
        response = self.client.get('/cnames/%s' % self.post_data['name'])
        self.assertEqual(response.status_code, 200)

    def test_cname_list_200_ok(self):
        """GET without name should return a list and 200 OK."""
        self.client.post('/cnames/', self.post_data)
        response = self.client.get('/cnames/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_cname_empty_list_200_ok(self):
        """GET without name should return a list and 200 OK."""
        response = self.client.get('/cnames/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_cname_post_hostname_in_use_400_bad_request(self):
        response = self.client.post('/cnames/', {'host': self.host_one['id'],
                                                 'name': self.host_two['name']})
        self.assertEqual(response.status_code, 400)

    def test_cname_post_nonexistant_host_400_bad_request(self):
        """Adding a cname with a unknown host will return 400 bad request."""
        response = self.client.post('/cnames/', {'host': 1,
                                                 'name': 'alias.example.org'})
        self.assertEqual(response.status_code, 400)

    def test_cname_post_name_not_in_a_zone_400_bad_requst(self):
        """Add a cname with a name without an existing zone if forbidden"""
        response = self.client.post('/cnames/', {'host': self.host_one['id'],
                                                 'name': 'host.example.com'})
        self.assertEqual(response.status_code, 400)

    def test_cname_patch_204_ok(self):
        """ Patching a cname should return 204 OK"""
        self.client.post('/cnames/', self.post_data)
        response = self.client.patch('/cnames/%s' % self.host_one['name'],
                                     {'ttl': '500',
                                      'name': 'new-alias.example.org'})
        self.assertEqual(response.status_code, 204)


class APINetworksTestCase(APITestCase):
    """"This class defines the test suite for api/networks """
    def setUp(self):
        """Define the test client and other variables."""
        self.client = get_token_client()
        self.network_sample = Network(range='10.0.0.0/24',
                                    description='some description',
                                    vlan=123,
                                    dns_delegated=False,
                                    category='so',
                                    location='Location 1',
                                    frozen=False)
        self.network_sample_two = Network(range='10.0.1.0/28',
                                        description='some description',
                                        vlan=135,
                                        dns_delegated=False,
                                        category='so',
                                        location='Location 2',
                                        frozen=False)

        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org')
        clean_and_save(self.host_one)
        clean_and_save(self.network_sample)
        clean_and_save(self.network_sample_two)

        self.patch_data = {
            'description': 'Test network',
            'vlan': '435',
            'dns_delegated': 'False',
            'category': 'si',
            'location': 'new-location'
        }

        self.patch_data_vlan = {'vlan': '435'}
        self.patch_data_range = {'range': '10.0.0.0/28'}
        self.patch_data_range_overlap = {'range': '10.0.1.0/29'}

        self.post_data = {
            'range': '192.0.2.0/29',
            'description': 'Test network',
            'vlan': '435',
            'dns_delegated': 'False',
        }
        self.post_data_bad_ip = {
            'range': '192.0.2.0.95/29',
            'description': 'Test network',
            'vlan': '435',
            'dns_delegated': 'False',
        }
        self.post_data_bad_mask = {
            'range': '192.0.2.0/2549',
            'description': 'Test network',
            'vlan': '435',
            'dns_delegated': 'False',
        }
        self.post_data_overlap = {
            'range': '10.0.1.0/29',
            'description': 'Test network',
            'vlan': '435',
            'dns_delegated': 'False',
        }

    def test_networks_post_201_created(self):
        """Posting a network should return 201"""
        response = self.client.post('/networks/', self.post_data)
        self.assertEqual(response.status_code, 201)

    def test_networks_post_400_bad_request_ip(self):
        """Posting a network with a range that has a malformed IP should return 400"""
        response = self.client.post('/networks/', self.post_data_bad_ip)
        self.assertEqual(response.status_code, 400)

    def test_networks_post_400_bad_request_mask(self):
        """Posting a network with a range that has a malformed mask should return 400"""
        response = self.client.post('/networks/', self.post_data_bad_mask)
        self.assertEqual(response.status_code, 400)

    def test_networks_post_409_overlap_conflict(self):
        """Posting a network with a range which overlaps existing should return 409"""
        response = self.client.post('/networks/', self.post_data_overlap)
        self.assertEqual(response.status_code, 409)

    def test_networks_get_200_ok(self):
        """GET on an existing ip-range should return 200 OK."""
        response = self.client.get('/networks/%s' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)

    def test_networks_list_200_ok(self):
        """GET without name should return a list and 200 OK."""
        response = self.client.get('/networks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_networks_patch_204_no_content(self):
        """Patching an existing and valid entry should return 204 and Location"""
        response = self.client.patch('/networks/%s' % self.network_sample.range, self.patch_data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['Location'], '/networks/%s' % self.network_sample.range)

    def test_networks_patch_204_non_overlapping_range(self):
        """Patching an entry with a non-overlapping range should return 204"""
        response = self.client.patch('/networks/%s' % self.network_sample.range, data=self.patch_data_range)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['Location'], '/networks/%s' % self.patch_data_range['range'])

    def test_networks_patch_400_bad_request(self):
        """Patching with invalid data should return 400"""
        response = self.client.patch('/networks/%s' % self.network_sample.range,
                                     data={'this': 'is', 'so': 'wrong'})
        self.assertEqual(response.status_code, 400)

    def test_networks_patch_404_not_found(self):
        """Patching a non-existing entry should return 404"""
        response = self.client.patch('/networks/193.101.168.0/29', self.patch_data)
        self.assertEqual(response.status_code, 404)

    def test_networks_patch_409_forbidden_range(self):
        """Patching an entry with an overlapping range should return 409"""
        response = self.client.patch('/networks/%s' % self.network_sample.range,
                data=self.patch_data_range_overlap)
        self.assertEqual(response.status_code, 409)

    def test_networks_get_network_by_ip_200_ok(self):
        """GET on an ip in a known network should return 200 OK."""
        response = self.client.get('/networks/ip/10.0.0.5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['range'], self.network_sample.range)

    def test_networks_get_network_unknown_by_ip_404_not_found(self):
        """GET on on an IP in a unknown network should return 404 not found."""
        response = self.client.get('/networks/ip/127.0.0.1')
        self.assertEqual(response.status_code, 404)

    def test_networks_get_usedcount_200_ok(self):
        """GET on /networks/<ip/mask>/used_count return 200 ok and data."""
        ip_sample = Ipaddress(host=self.host_one, ipaddress='10.0.0.17')
        clean_and_save(ip_sample)

        response = self.client.get('/networks/%s/used_count' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 1)

    def test_networks_get_usedlist_200_ok(self):
        """GET on /networks/<ip/mask>/used_list should return 200 ok and data."""
        ip_sample = Ipaddress(host=self.host_one, ipaddress='10.0.0.17')
        clean_and_save(ip_sample)

        response = self.client.get('/networks/%s/used_list' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ['10.0.0.17'])

    def test_networks_get_unusedcount_200_ok(self):
        """GET on /networks/<ip/mask>/unused_count should return 200 ok and data."""
        ip_sample = Ipaddress(host=self.host_one, ipaddress='10.0.0.17')
        clean_and_save(ip_sample)

        response = self.client.get('/networks/%s/unused_count' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 250)

    def test_networks_get_unusedlist_200_ok(self):
        """GET on /networks/<ip/mask>/unused_list should return 200 ok and data."""
        ip_sample = Ipaddress(host=self.host_one, ipaddress='10.0.0.17')
        clean_and_save(ip_sample)

        response = self.client.get('/networks/%s/unused_list' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 250)

    def test_networks_get_first_unused_200_ok(self):
        """GET on /networks/<ip/mask>/first_unused should return 200 ok and data."""
        ip_sample = Ipaddress(host=self.host_one, ipaddress='10.0.0.17')
        clean_and_save(ip_sample)

        response = self.client.get('/networks/%s/first_unused' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '10.0.0.4')

    def test_networks_get_ptroverride_list(self):
        """GET on /networks/<ip/mask>/ptroverride_list should return 200 ok and data."""
        response = self.client.get('/networks/%s/ptroverride_list' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
        ptr = PtrOverride(host=self.host_one, ipaddress='10.0.0.10')
        clean_and_save(ptr)
        response = self.client.get('/networks/%s/ptroverride_list' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ['10.0.0.10'])

    def test_networks_get_reserved_list(self):
        """GET on /networks/<ip/mask>/reserverd_list should return 200 ok and data."""
        response = self.client.get('/networks/%s/reserved_list' % self.network_sample.range)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, ['10.0.0.0', '10.0.0.1',
            '10.0.0.2', '10.0.0.3','10.0.0.255'])

    def test_networks_delete_204_no_content(self):
        """Deleting an existing entry with no adresses in use should return 204"""
        response = self.client.post('/networks/', self.post_data)
        self.assertEqual(response.status_code, 201)
        response = self.client.delete('/networks/%s' % self.post_data['range'])
        self.assertEqual(response.status_code, 204)

    def test_networks_delete_409_conflict(self):
        """Deleting an existing entry with  adresses in use should return 409"""
        response = self.client.post('/networks/', self.post_data)
        self.assertEqual(response.status_code, 201)

        ip_sample = Ipaddress(host=self.host_one, ipaddress='192.0.2.1')
        clean_and_save(ip_sample)

        response = self.client.delete('/networks/%s' % self.post_data['range'])
        self.assertEqual(response.status_code, 409)


class APIModelChangeLogsTestCase(APITestCase):
    """This class defines the test suite for api/history """

    def setUp(self):
        """Define the test client and other variables."""
        self.client = get_token_client()
        self.host_one = Host(name='some-host.example.org',
                             contact='mail@example.org',
                             ttl=300,
                             loc='23 58 23 N 10 43 50 E 80m',
                             comment='some comment')
        clean_and_save(self.host_one)

        self.log_data = {'host': self.host_one.id,
                         'name': self.host_one.name,
                         'contact': self.host_one.contact,
                         'ttl': self.host_one.ttl,
                         'loc': self.host_one.loc,
                         'comment': self.host_one.comment}

        self.log_entry_one = ModelChangeLog(table_name='hosts',
                                            table_row=self.host_one.id,
                                            data=self.log_data,
                                            action='saved',
                                            timestamp=timezone.now())
        clean_and_save(self.log_entry_one)

    def test_history_get_200_OK(self):
        """Get on /history/ should return a list of table names that have entries, and 200 OK."""
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('hosts', response.data)

    def test_history_host_get_200_OK(self):
        """Get on /history/hosts/<pk> should return a list of dicts containing entries for that host"""
        response = self.client.get('/history/hosts/{}'.format(self.host_one.id))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
