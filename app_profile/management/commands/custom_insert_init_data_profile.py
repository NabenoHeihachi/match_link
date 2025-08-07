# =================================
# カスタムコマンド: タグ初期データ登録
# =================================
from django.core.management.base import BaseCommand, CommandError
from app_profile.models.options_model import ValueTagModel, HobbyTagModel, CommunicationTagModel
from common.util_message import UtilMessage
from django.db import transaction

class Command(BaseCommand):
    help = "タグ初期データを登録します。"

    def handle(self, *args, **options):
        """
        初期データ登録処理
        """
        # ================
        # 例外処理:START
        # ================
        try:
            # -----------------
            # 存在確認
            # -----------------
            if ValueTagModel.objects.exists():
                print(UtilMessage.Database.E_ALREADY_REGISTERED.format('バリュータグデータ'))
                return
            if HobbyTagModel.objects.exists():
                print(UtilMessage.Database.E_ALREADY_REGISTERED.format('趣味タグデータ'))
                return
            if CommunicationTagModel.objects.exists():
                print(UtilMessage.Database.E_ALREADY_REGISTERED.format('コミュニケーションタグデータ'))
                return

            # -----------------
            # 情報の取得
            # -----------------
            insert_user = "init_custom_command"
            
            value_tag_objects = [
                ValueTagModel(tag_name="挑戦", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="誠実", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="協調性", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="柔軟性", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="責任感", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="丁寧さ", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="スピード重視", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="成果重視", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="探究心", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="独立心", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="思いやり", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="礼儀", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="信頼", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="公正さ", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="創造性", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="向上心", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="自己管理", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="健康志向", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="安定志向", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="挑発心", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="勤勉さ", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="自分らしさ", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="冒険心", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="学び続ける姿勢", created_by=insert_user, updated_by=insert_user),
                ValueTagModel(tag_name="ユーモア", created_by=insert_user, updated_by=insert_user),
            ]

            hobby_tag_objects = [
                HobbyTagModel(tag_name="映画鑑賞", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="読書", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="音楽鑑賞", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="料理", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="散歩", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="旅行", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="ゲーム", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="アニメ・漫画", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="写真撮影", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="運動・ジム", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="手芸", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="DIY", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="釣り", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="キャンプ", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="カフェ巡り", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="英語学習", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="ペットと遊ぶ", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="プログラミング", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="ボードゲーム", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="イラスト", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="スポーツ観戦", created_by=insert_user, updated_by=insert_user),
                HobbyTagModel(tag_name="日記・ブログ", created_by=insert_user, updated_by=insert_user),
            ]

            communication_tag_objects = [
                CommunicationTagModel(tag_name="聞き役タイプ", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="発信タイプ", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="共感型", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="論理型", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="テンション高め", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="落ち着きタイプ", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="リアクション多め", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="聞き上手", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="控えめ", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="率直", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="丁寧語重視", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="フレンドリー", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="質問型", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="アイデア型", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="共通点探し型", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="一言多いタイプ", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="感情表現豊か", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="情報共有型", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="ボディランゲージ多め", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="空気読み重視", created_by=insert_user, updated_by=insert_user),
                CommunicationTagModel(tag_name="沈黙もOK", created_by=insert_user, updated_by=insert_user),
            ]

            # -------------------
            # 情報登録
            # -------------------
            try:
                # トランザクション開始
                with transaction.atomic():
                    ValueTagModel.objects.bulk_create(value_tag_objects)
                    HobbyTagModel.objects.bulk_create(hobby_tag_objects)
                    CommunicationTagModel.objects.bulk_create(communication_tag_objects)

            except Exception as e:
                print("例外詳細:", str(e))
                # コマンドエラー
                raise CommandError(UtilMessage.Database.E_SAVE.format("タグ初期データ", str(e)))
                return
            
            
            # 成功メッセージ表示
            self.stdout.write(
                self.style.SUCCESS(UtilMessage.Command.S_ACTION_SUCCESS.format('タグ初期データ登録'))
            )
            return

        # ================
        # 例外処理:END
        # ================
        except KeyboardInterrupt:
            # キーボード割り込み
            self.stdout.write(self.style.WARNING(
                UtilMessage.Command.W_ACTION_CANCEL.format('タグ初期データ登録')
            ))
            return
        except CommandError as e:
            # コマンドエラー
            raise e
        except Exception as e:
            # コマンドエラー
            raise CommandError(
                UtilMessage.Command.E_EXCECTION.format('タグ初期データ登録', str(e))
            )
        

