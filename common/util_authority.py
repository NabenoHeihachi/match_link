# =================================
# UTIL:アカウントコードクラス
# =================================
class UtilAuthority:
    _ACCOUNT_AUTH_CODE_DICT = {
        # 管理アカウント：組織を管理するためのアカウント
        "管理アカウント": "0",
        # メンバーアカウント　　：組織に所属する一般アカウント
        "メンバーアカウント": "10",
    }

    @classmethod
    def get_dict(cls) -> dict:
        """元の辞書（ラベル→コード）を返す"""
        return cls._ACCOUNT_AUTH_CODE_DICT.copy()

    @classmethod
    def get_reversed_dict(cls) -> dict:
        """コード→ラベルの辞書を返す"""
        return {v: k for k, v in cls._ACCOUNT_AUTH_CODE_DICT.items()}

    @classmethod
    def to_code(cls, label: str) -> str | None:
        """ラベルからコードを取得"""
        return cls._ACCOUNT_AUTH_CODE_DICT.get(label)

    @classmethod
    def to_label(cls, code: str) -> str | None:
        """コードからラベルを取得"""
        return cls.get_reversed_dict().get(code)
    
    @classmethod
    def is_valid_code(cls, code: str) -> bool:
        """コードが有効かどうかをチェック"""
        return code in cls._ACCOUNT_AUTH_CODE_DICT.values()
    
    @classmethod
    def is_valid_label(cls, label: str) -> bool:
        """ラベルが有効かどうかをチェック"""
        return label in cls._ACCOUNT_AUTH_CODE_DICT.keys()
    
    @classmethod
    def is_manager(cls, code: str) -> bool:
        """コードが管理用アカウントかどうかをチェック"""
        return code in cls._ACCOUNT_AUTH_CODE_DICT["管理アカウント"]
    
    @classmethod
    def is_staff(cls, code: str) -> bool:
        """コードが一般アカウントかどうかをチェック"""
        return code in cls._ACCOUNT_AUTH_CODE_DICT["一般アカウント"]
