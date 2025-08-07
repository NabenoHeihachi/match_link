# =================================
# UTIL: バリデーション関数
# =================================
import re
import uuid
from datetime import datetime

class UtilValidation:
    """
    バリデーション系ユーティリティクラス
    概要: 入力値のバリデーションを行うためのユーティリティ関数を提供
    """

    def is_length_valid(input_text:str, min_length:int, max_length:int) -> bool:
        """
        入力の文字数が指定範囲内であるかをチェック
        ---
        params
            input_text 入力値
            min_length 文字数最小値
            max_length 文字数最大値
        returns
            bool 
                ture 長さ範囲内
                false 長さ範囲外
        """
        # 結果を返却
        return bool(min_length <= len(input_text) <= max_length)

    def is_convertible_to_number(input_text:str) -> bool:
        """
        入力が数字に変換可能であるかをチェック
        ---
        params
            input_text 入力値
        returns
            bool 
                ture 変換可能
                false 変換不可
        """
        # 数値に返却できる場合
        try:
            # 整数または小数に変換
            float(input_text) 
            # tureを返却
            return True
        # 数値に返却できない場合
        except ValueError:
            # falseを返却
            return False

    def has_special_characters(input_text:str) -> bool:
        """
        入力に特殊記号が含まれていないかをチェック
        （半角英数字と空白以外の文字を検出）
        ---
        params
            input_text 入力値
        returns
            bool 
                ture 含まれている
                false 含まれていない
        """
        # 特殊文字リスト
        special_characters = [
            "\\",  # 制御文字
            "<", ">", "&", "/", "'", '"',  # スクリプト関連文字
            "--", ";", "#", "=",  # SQLインジェクション関連文字
            "|", "¥", "*", "..", "~", "+", ":", "$"  # その他
        ]
        # 特殊文字でループ
        for special_character in special_characters:
            # 特殊文字が見つかった場合
            if special_character in input_text:
                # tureを返却
                return True
        # 特殊文字が見つからない場合
        return False

    def is_not_empty(input_text:str) -> bool:
        """
        入力が空でないかをチェック
        ---
        params
            input_text 入力値
        returns
            bool 
                ture 空値
                false 空値でない
        """
        # None 空値の場合
        if input_text != None and input_text != "":
            # tureを返却
            return True
        # None 空値でない場合
        else:
            # falseを返却
            return False

    def is_match(input_text: str, pattern_type: str) -> bool:
        """
        指定した正規表現に入力値がマッチしているかチェック
        
        params:
            input_text (str): チェックする文字列
            pattern_type (str): 正規表現パターンタイプ「user_id, password」
        
        returns:
            bool: マッチしている場合はTrue、そうでない場合はFalse
        """
        # 正規表現初期値
        pattern = ""

        # ユーザーIDの場合
        if pattern_type == "user_id":
            # 半角英数字大文字小文字８から３２文字
            pattern = r"^[A-Za-z0-9]{8,32}$"
        # パスワードの場合
        elif pattern_type == "password":
            # 半角英数字大文字小文字記号「!,?,(,),@」８から６４文字
            pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!?()@])[A-Za-z\d!?()@]{8,64}$"
        # メールの場合
        elif pattern_type == "email":
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,256}$"
        # 学生番号の場合
        elif pattern_type == "student_number":
            pattern = r"^[0-9]{8}$"
        # システムコードの場合
        elif pattern_type == "system_code":
            # 半角数字2文字
            pattern = r"^[0-9]{2}$"

        # 結果を返却
        return bool(re.fullmatch(pattern, input_text))
    
    def is_valid_time(input_time: str) -> bool:
        """
        入力された文字列が時間形式として有効かチェック

        Args:
            input_time (str): 時間文字列 (例: "14:30")
        
        Returns:
            bool: 有効な時間形式であれば True、それ以外は False
        """
        try:
            # 時間形式で解析を試みる
            datetime.strptime(input_time, "%H:%M")
            return True
        except ValueError:
            return False

    def is_valid_date(input_date: str) -> bool:
        """
        入力された文字列が年月日形式として有効かチェック

        Args:
            input_date (str): 日付文字列 (例: "2025-01-10")
        
        Returns:
            bool: 有効な日付形式であれば True、それ以外は False
        """
        try:
            # 年月日形式で解析を試みる
            datetime.strptime(input_date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def is_valid_month(input_month: str) -> bool:
        """
        入力された文字列が年月形式として有効かチェック

        Args:
            input_date (str): 日付文字列 (例: "2025-01")
        
        Returns:
            bool: 有効な日付形式であれば True、それ以外は False
        """
        try:
            # 年月形式で解析を試みる
            datetime.strptime(input_month, "%Y-%m")
            return True
        except ValueError:
            return False
    
    def is_time_before(enter_time: str, exit_time: str) -> bool:
        """
        2つの時刻文字列を比較し、enter_timeがexit_time よりも前かどうかチェック

        Args:
            enter_time (str): 比較対象となる最初の時刻（フォーマット: HH:MM）
            exit_time (str): 比較対象となる2つ目の時刻（フォーマット: HH:MM）

        Returns:
            bool: enter_time が exit_time よりも前であれば True、それ以外は False
        """

        # 時刻を datetime オブジェクトに変換
        enter_time = datetime.strptime(enter_time, "%H:%M")
        exit_time = datetime.strptime(exit_time, "%H:%M")
        # 比較して結果を返す
        return bool(enter_time <= exit_time)
    
    def is_date_before(start_date: str, end_date: str) -> bool:
        """
        2つの日時文字列を比較し、start_dateがend_date よりも前かどうかチェック

        Args:
            start_date (str): 比較対象となる最初の時刻
            end_date (str): 比較対象となる2つ目の時刻

        Returns:
            bool: start_date が end_date よりも前であれば True、それ以外は False
        """

        # 時刻を datetime オブジェクトに変換
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        # 比較して結果を返す
        return bool(start_date <= end_date)
    
    def is_uuid(input_text: str) -> bool:
        """
        入力がUUID形式であるかをチェック

        Args:
            input_text (str): チェックする文字列

        Returns:
            bool: UUID形式であればTrue、そうでなければFalse
        """
        try:
            # UUIDを生成してみる
            uuid.UUID(input_text)
            return True
        except ValueError:
            return False