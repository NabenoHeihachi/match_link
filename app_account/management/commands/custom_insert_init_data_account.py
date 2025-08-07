# =================================
# カスタムコマンド: ユーザー作成
# =================================
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from app_account.models.subscription_model import SubscriptionModel
from app_account.models.organization_model import OrganizationModel
from app_account.models.account_model import AccountModel
from common.util_message import UtilMessage
from common.util_authority import UtilAuthority
from django.conf import settings
from django.db import transaction

class Command(BaseCommand):
    help = "アカウント初期データを登録します。"

    def handle(self, *args, **options):
        """
        アカウント初期データ登録処理
        """
        # ================
        # 例外処理:START
        # ================
        try:
            # -----------------
            # 存在確認
            # -----------------
            if OrganizationModel.objects.exists():
                print(UtilMessage.Database.E_ALREADY_REGISTERED.format('組織データ'))
                return
            if AccountModel.objects.exists():
                print(UtilMessage.Database.E_ALREADY_REGISTERED.format('アカウントデータ'))
                return
            if SubscriptionModel.objects.exists():
                print(UtilMessage.Database.E_ALREADY_REGISTERED.format('サブスクリプションデータ'))
                return

            # -----------------
            # 情報の取得
            # -----------------
            init_account_id = settings.INIT_ACCOUNT_ID
            init_password = settings.INIT_PASSWORD

            subscription_objects = [
                SubscriptionModel(
                    subscription_name="Free",
                    subscription_description="少人数のチームや個人利用に最適です。基本的な相性分析機能をお使いいただけます。",
                    subscription_price=0,
                    created_by="init_custom_command",
                    updated_by="init_custom_command"
                ),
                SubscriptionModel(
                    subscription_name="Standard",
                    subscription_description="中規模のチームや個人利用に最適です。基本的な相性分析機能をお使いいただけます。",
                    subscription_price=8000,
                    account_limit=50,
                    matching_group_limit=10,
                    is_ai_enabled=True,
                    created_by="init_custom_command",
                    updated_by="init_custom_command"
                ),
                SubscriptionModel(
                    subscription_name="Enterprise",
                    subscription_description="大規模のチームや個人利用に最適です。基本的な相性分析機能をお使いいただけます。",
                    subscription_price=160000,
                    account_limit=100,
                    matching_group_limit=30,
                    is_ai_enabled=True,
                    created_by="init_custom_command",
                    updated_by="init_custom_command"
                )
            ]

            # -------------------
            # 情報登録
            # -------------------
            try:
                # トランザクション開始
                with transaction.atomic():
                    SubscriptionModel.objects.bulk_create(subscription_objects)

                    # Freeプランの取得
                    free_subscription = SubscriptionModel.objects.get(subscription_name="Free")

                    init_organization = OrganizationModel.objects.create(
                        organization_name="Default Organization",
                        organization_description="Default organization for initial setup.",
                        organization_email="info@example.com",
                        subscription=free_subscription,
                        created_by="init_custom_command",
                        updated_by="init_custom_command"
                    )

                    AccountModel.objects.create(
                        account_id=str(init_organization.organization_id) + init_account_id,
                        password=make_password(init_password),
                        account_name="初期管理者",
                        account_description="初期管理者アカウント",
                        organization=init_organization,
                        auth_code=UtilAuthority.get_dict().get('管理アカウント'),
                        is_staff=True,
                        is_superuser=True,
                        created_by="init_custom_command",
                        updated_by="init_custom_command"
                    )

            except Exception as e:
                print("例外詳細:", str(e))
                # コマンドエラー
                raise CommandError(UtilMessage.Database.E_SAVE.format("アカウント初期データ", str(e)))
                return
            
            
            # 成功メッセージ表示
            self.stdout.write(
                self.style.SUCCESS(UtilMessage.Command.S_ACTION_SUCCESS.format('アカウント初期データ登録'))
            )
            return

        # ================
        # 例外処理:END
        # ================
        except KeyboardInterrupt:
            # キーボード割り込み
            self.stdout.write(self.style.WARNING(
                UtilMessage.Command.W_ACTION_CANCEL.format('アカウント初期データ登録')
            ))
            return
        except CommandError as e:
            # コマンドエラー
            raise e
        except Exception as e:
            # コマンドエラー
            raise CommandError(
                UtilMessage.Command.E_EXCECTION.format('アカウント初期データ登録', str(e))
            )
        

