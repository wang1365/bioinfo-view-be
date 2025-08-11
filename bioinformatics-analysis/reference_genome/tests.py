from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from account.models import Account
from .models import ReferenceGenome


class ReferenceGenomeModelTest(TestCase):
    """自建参考基因组模型测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            username='testuser'
        )
    
    def test_create_reference_genome(self):
        """测试创建参考基因组"""
        genome = ReferenceGenome.objects.create(
            custom_database='test_db',
            virus_name={'name': 'SARS-CoV-2'},
            virus_type={'type': 'RNA virus'},
            host='Human',
            host_genome_version='GRCh38',
            host_seq_file='/path/to/host.fasta',
            virus_seq_file='/path/to/virus.fasta',
            host_info={'length': 3000000000},
            virus_info={'length': 30000},
            creator=self.account
        )
        
        self.assertEqual(genome.custom_database, 'test_db')
        self.assertEqual(genome.host, 'Human')
        self.assertFalse(genome.is_deleted)
        self.assertEqual(str(genome), 'test_db - Human')
    
    def test_soft_delete(self):
        """测试软删除"""
        genome = ReferenceGenome.objects.create(
            custom_database='test_db',
            virus_name={'name': 'SARS-CoV-2'},
            virus_type={'type': 'RNA virus'},
            host='Human',
            host_genome_version='GRCh38',
            host_seq_file='/path/to/host.fasta',
            virus_seq_file='/path/to/virus.fasta',
            creator=self.account
        )
        
        genome.soft_delete()
        self.assertTrue(genome.is_deleted)
    
    def test_get_active_objects(self):
        """测试获取活跃对象"""
        # 创建一个正常的记录
        active_genome = ReferenceGenome.objects.create(
            custom_database='active_db',
            virus_name={'name': 'SARS-CoV-2'},
            virus_type={'type': 'RNA virus'},
            host='Human',
            host_genome_version='GRCh38',
            host_seq_file='/path/to/host.fasta',
            virus_seq_file='/path/to/virus.fasta',
            creator=self.account
        )
        
        # 创建一个已删除的记录
        deleted_genome = ReferenceGenome.objects.create(
            custom_database='deleted_db',
            virus_name={'name': 'SARS-CoV-2'},
            virus_type={'type': 'RNA virus'},
            host='Human',
            host_genome_version='GRCh38',
            host_seq_file='/path/to/host.fasta',
            virus_seq_file='/path/to/virus.fasta',
            creator=self.account,
            is_deleted=True
        )
        
        active_objects = ReferenceGenome.get_active_objects()
        self.assertEqual(active_objects.count(), 1)
        self.assertEqual(active_objects.first(), active_genome)


class ReferenceGenomeAPITest(APITestCase):
    """自建参考基因组API测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            username='testuser'
        )
        
        self.test_data = {
            'custom_database': 'test_db',
            'virus_name': {'name': 'SARS-CoV-2'},
            'virus_type': {'type': 'RNA virus'},
            'host': 'Human',
            'host_genome_version': 'GRCh38',
            'host_seq_file': '/path/to/host.fasta',
            'virus_seq_file': '/path/to/virus.fasta',
            'host_info': {'length': 3000000000},
            'virus_info': {'length': 30000}
        }
    
    def test_create_reference_genome_unauthorized(self):
        """测试未授权创建参考基因组"""
        response = self.client.post('/reference-genomes/', self.test_data)
        # 由于没有认证，应该返回401或403
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_list_reference_genomes_unauthorized(self):
        """测试未授权获取参考基因组列表"""
        response = self.client.get('/reference-genomes/')
        # 由于没有认证，应该返回401或403
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])