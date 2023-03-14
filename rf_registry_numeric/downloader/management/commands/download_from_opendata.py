import ssl
import time
import urllib

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from registry.models import Registry


class Command(BaseCommand):
    help = """Download and import to local db files from
    https://opendata.digital.gov.ru/registry/numeric/downloads/"""
    download_url_list = [
        "https://opendata.digital.gov.ru/downloads/ABC-3xx.csv",
        "https://opendata.digital.gov.ru/downloads/ABC-4xx.csv",
        "https://opendata.digital.gov.ru/downloads/ABC-8xx.csv",
        "https://opendata.digital.gov.ru/downloads/DEF-9xx.csv",
    ]

    @staticmethod
    def _global_setup():
        ssl._create_default_https_context = ssl._create_unverified_context

    @staticmethod
    def _get_no_cache_url(url: str) -> str:
        cur_unix_time = int(time.time())
        return f"{url}?{cur_unix_time}"

    @staticmethod
    def _get_and_parse(url: str) -> pd.DataFrame:
        df = pd.read_csv(
            url,
            names=[
                "code",
                "start",
                "end",
                "size",
                "operator",
                "region",
                "tax_number",
            ],
            dtype={
                "code": "int64",
                "start": "int64",
                "end": "int64",
                "size": "int64",
                "operator": "str",
                "region": "str",
                "tax_number": "float",
            },
            delimiter=";",
            header=0,
        )
        return df

    @staticmethod
    def _clear_registry():
        Registry.objects.all().delete()

    @staticmethod
    def _save_in_registry(row: pd.Series) -> Registry:
        row = Command._normalize_row(row)
        obj = Registry(**row)
        obj.save()
        return obj

    @staticmethod
    def _normalize_row(row: pd.Series) -> dict:
        if pd.isna(row["tax_number"]):
            row["tax_number"] = None
        row = row.to_dict()
        return row

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start"))
        Command._global_setup()
        Command._clear_registry()
        for url in self.download_url_list:
            url = Command._get_no_cache_url(url)
            self.stdout.write(self.style.NOTICE(f"Try download {url}"))
            try:
                df = Command._get_and_parse(url)
            except urllib.error.URLError as e:
                self.stdout.write(self.style.ERROR(f"Cant download {url} Error: {e}"))
                continue
            for _, row in df.iterrows():
                Command._save_in_registry(row)
        self.stdout.write(self.style.SUCCESS("Finish"))
