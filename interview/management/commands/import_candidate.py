import csv

from django.core.management import BaseCommand
from interview.models import Candidate


# pytho manage.py import_candidate --path file.csv

class Command(BaseCommand):
    help = '从一个CSV文件中读取候选人列表，导入到数据库中'

    # 定义命令行参数 为长参数
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        with open(path, 'rt', encoding='gbk') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                print(row[0])
                print(row[1])
                candidate = Candidate.objects.create(
                    username=row[0],
                    city=row[1],
                    phone=row[2],
                    bachelor_school=row[3],
                    major=row[4],
                    degree=row[5],
                    test_score_of_general_ability=row[6],
                    paper_score=row[7]
                )
                print(candidate)
