import requests
from django.conf import settings
from app_account.models.account_model import AccountModel
from app_profile.models.personality_model import PersonalityModel

LLM_API_URL = settings.LLM_API_URL
LLM_MODEL = settings.LLM_MODEL

class UtilLLM:
    @staticmethod
    def generate_match_reason(
        target_account: AccountModel, 
        candidate_account: AccountModel, 
        model=LLM_MODEL) -> str:

        target_personality = PersonalityModel.objects.get(account=target_account)
        candidate_personality = PersonalityModel.objects.get(account=candidate_account)

        # プラン確認
        if target_personality.organization.subscription and not target_personality.organization.subscription.is_ai_enabled:
            return "FreeプランではAIサマリー機能は利用できません。"

        target_personality_communication_tags = ', '.join(target_personality.communication_tags.values_list('tag_name', flat=True))
        candidate_personality_communication_tags = ', '.join(candidate_personality.communication_tags.values_list('tag_name', flat=True))

        target_personality_hobby_tags = ', '.join(target_personality.hobby_tags.values_list('tag_name', flat=True))
        candidate_personality_hobby_tags = ', '.join(candidate_personality.hobby_tags.values_list('tag_name', flat=True))

        target_personality_value_tags = ', '.join(target_personality.value_tags.values_list('tag_name', flat=True))
        candidate_personality_value_tags = ', '.join(candidate_personality.value_tags.values_list('tag_name', flat=True))

        prompt = f"""
あなたは性格心理学に基づくマッチングアドバイザーです。
以下は上司・部下マッチングにおける対象者と候補者のプロフィールです。
それぞれの性格や価値観、趣味、コミュニケーションスタイルの違いから、
「この二人がなぜ相性が良いのか」を、優しく・納得感のある日本語で簡潔に100文字程度で説明してください。

[対象者]
外向性: {target_personality.big_five_extraversion}
情緒安定性: {target_personality.big_five_neuroticism}
開放性: {target_personality.big_five_openness}
協調性: {target_personality.big_five_agreeableness}
誠実性: {target_personality.big_five_conscientiousness}
コミュニケーションスタイル: {target_personality_communication_tags}
趣味: {target_personality_hobby_tags}
価値観: {target_personality_value_tags}

[候補者]
外向性: {candidate_personality.big_five_extraversion}
情緒安定性: {candidate_personality.big_five_neuroticism}
開放性: {candidate_personality.big_five_openness}
協調性: {candidate_personality.big_five_agreeableness}
誠実性: {candidate_personality.big_five_conscientiousness}
コミュニケーションスタイル: {candidate_personality_communication_tags}
趣味: {candidate_personality_hobby_tags}
価値観: {candidate_personality_value_tags}

→ 相性の説明（日本語）:
"""

        try:
            # LLM APIにリクエストを送信
            response = requests.post(LLM_API_URL, json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }, timeout=30)

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip() or "生成に失敗しました。"
            else:
                return "生成に失敗しました。"
        except Exception as e:
            return "生成に失敗しました。"