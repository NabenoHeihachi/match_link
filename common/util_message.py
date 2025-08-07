
# =================================
# UTIL: メッセージクラス
# =================================
class UtilMessage:
    """
    メッセージ系ユーティリティクラス
    概要: アプリケーション内で使用するメッセージを管理するためのユーティリティ関数を提供
    """

    class Validation:
        """
        バリデーションメッセージ
        概要: 入力値のバリデーションに関するメッセージを管理
        """
        # ERROR
        E_PLZ_CHECK = "入力内容に誤りがあります。再度確認してください。"
        E_PLZ_INP = "{0}を入力してください。"
        E_PLZ_INP_LENGTH = "{0}を{1}文字以上{2}文字以内で入力してください。"
        E_PLZ_SELECT = "{0}を選択してください。"
        E_PLZ_INP_TIMESTAMP = "{0}を時刻形式で入力してください。"
        E_PLZ_INP_DATE = "{0}を日付形式で入力してください。"
        E_PLZ_INP_EMAIL = "{0}をメールアドレス形式で入力してください。"
        E_PLZ_INP_NUM = "{0}を数値形式で入力してください。"
        E_INVALID_INPUT = "入力された{0}はご利用できません。"
        E_INVALID_CHAR = "{0}に使用できない文字が含まれています。"
        E_INVALID_TIME_ORDER = "{0}は{1}よりも前の時刻を入力してください。"
        E_INVALID_DATE_ORDER = "{0}は{1}よりも前の日付を入力してください。"
        E_INVALID_ID = "{0}IDが不正です。再度ページを読み直してからお試しください。"
        E_INVALID_ONE_TIME_PASSWORD = "ワンタイムパスワードが一致しません。再度お試しください。"
        E_INVALID_STUDENT_NUMBER = "{0}は、半角数字8文字で入力してください。"
        E_INVALID_USER_ID = "ユーザーIDは、半角の英大文字・小文字・数字から構成し、8文字以上32文字以内で入力してください。"
        E_INVALID_PASSWORD = "パスワードは、半角の英大文字・小文字・数字・記号「!,?,(,),@」から構成し、8文字以上64文字以内で入力してください。"
        E_INVALID_SYSTEM_CODE = "{0}コードは、半角数字2文字で入力してください。"
        E_INVALID_PASSWORD_CONFIRM = "パスワードが一致しません。再度入力してください。"
        E_INVALID_ACCOUNT = "このアカウントは、{0}ご利用できません。"
        E_TERMS_REQUIRED = "ご利用には「利用規約」と「個人情報保護方針」に同意する必要があります。"
        E_AUTH_FAILED = "ユーザー名またはパスワードが正しくありません。"
        E_NOT_AUTHORIZED = "この操作を行う権限がありません。"

    class Database:
        """
        データベースメッセージ
        概要: データベース操作に関するメッセージを管理
        """
        # SUCCESS
        S_SAVE = "{0}が正常に保存されました。"
        S_DELETE = "{0}が正常に削除されました。"
        S_UPDATE = "{0}が正常に更新されました。"
        S_CREATE = "{0}が正常に作成されました。"
        # WARNING
        W_NOT_FOUND = "{0}は見つかりませんでした。"
        # ERROR
        E_ALREADY_REGISTERED = "{0}はすでに登録されています。"
        E_SAVE = "{0}保存中に予期しないエラーが発生しました。"
        E_DELETE = "{0}削除中に予期しないエラーが発生しました。"
        E_UPDATE = "{0}更新中に予期しないエラーが発生しました。"
        E_CREATE = "{0}作成中に予期しないエラーが発生しました。"
    
    class Command:
        """
        コマンドメッセージ
        概要: システムコマンドに関するメッセージを管理
        """
        # SUCCESS
        S_ACTION_SUCCESS = "\n\n{0}処理が正常に完了しました。"
        # ERROR
        E_EXCECTION = "\n{0}処理中に予期しないエラーが発生しました: {1}"
        # WARNING
        W_ACTION_CANCEL = "\n{0}処理はキャンセルされました。"

    class Browser:
        """
        ブラウザメッセージ
        概要: ブラウザ操作に関するメッセージを管理
        """
        # INFO
        I_LOADING = "読み込み中..."
        I_SAVING = "保存中..."
        I_DELETING = "削除中..."
        I_PLZ_ACTION = "{0}してください。"
        # SUCCESS
        S_ACTION_SUCCESS = "{0}処理が正常に完了しました。"
        # WARNING
        W_MISSING_ENTRY_RECORD = "指定期間内に、施設利用中または入退室時間が記録されていないデータがあります。"
        # ERROR
        E_PLZ_ACTIO = "{0}してください。"
        E_ACTION_ERROR = "{0}処理に失敗しました。再度お試しください。"
        E_NOT_AUTHORIZED = "必要な権限がありません。"
        E_INVALID_REQUEST = "無効なリクエストです。再度お試しください。"
        E_FILE_NOT_FOUND = "{0}ファイルが見つかりません。"
    
    class Log:
        """
        ログメッセージ
        概要: システムログに関するメッセージを管理
        """
        # INFO
        I_VIEW_GET = "-----【{0} 処理:GET】-----"
        I_VIEW_POST = "-----【{0} 処理:POST】-----"
        I_VIEW_SSE = "-----【{0} 処理:SSE】-----"
        # ERROR
        E_EXCEPT_GET = "EXCEPTION ERROR【{0} 処理:GET 】: {1}"
        E_EXCEPT_POST = "EXCEPTION ERROR【{0} 処理:POST 】: {1}"
        E_EXCEPT_SSE = "EXCEPTION ERROR【{0} 処理:SSE 】: {1}"
