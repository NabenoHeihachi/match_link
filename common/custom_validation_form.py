import re
from django import forms
from django.core.exceptions import ValidationError

DANGEROUS_PATTERNS = [
    r"<script.*?>.*?</script.*?>",  # <script>タグ
    r"javascript:",                # javascriptスキーム
    r"on\w+\s*=",                  # onclick=などのイベント属性
    r"[|&;$`]",                    # コマンドインジェクション文字
    r"(--|\b(SELECT|UPDATE|DELETE|INSERT|DROP)\b)",  # SQL風
]

def validate_no_dangerous_input(value):
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, value, flags=re.IGNORECASE):
            raise ValidationError("不正な文字列が含まれています")