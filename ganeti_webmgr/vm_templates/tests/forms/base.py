from django.contrib.auth.models import User
from django.test import TestCase

from ganeti_webmgr.django_test_tools.users import UserTestMixin

from ganeti_webmgr.vm_templates.models import VirtualMachineTemplate
from ganeti_webmgr.clusters.models import Cluster


class TemplateTestCase(TestCase, UserTestMixin):
    def setUp(self):
        # Cluster
        cluster = Cluster(hostname='test.cluster.gwm', slug='test',
                          username='foo', password='bar')
        # cluster.info = INFO
        cluster.save()

        # Template
        template_data = dict(
            template_name='new.vm.template',
            description='A new template.',
            cluster=cluster.id,
            start=True,
            name_check=True,
            disk_template='plain',
            disk_count=0,
            memory=256,
            vcpus=2,
            root_path='/',
            kernel_path='',
            cdrom_image_path='',
            serial_console=False,
            nic_type='paravirtual',
            disk_type='paravirtual',
            nic_count=0,
            boot_order='disk',
            os='image+ubuntu-lucid',
        )
        data = template_data.copy()
        data['cluster'] = cluster
        del data['disk_count']
        del data['nic_count']
        template = VirtualMachineTemplate(**data)
        template.save()

        # Template Fields
        fields = vars(template).keys()

        # Users
        self.create_users([
            ('superuser', {'is_superuser': True}),
            'cluster_admin',
        ])
        self.cluster_admin.grant('admin', cluster)

        self.users = [self.superuser, self.cluster_admin]
        self.template = template
        self.cluster = cluster
        self.template_data = template_data
        self.template_fields = fields

    def tearDown(self):
        User.objects.all().delete()
        Cluster.objects.all().delete()
        VirtualMachineTemplate.objects.all().delete()
