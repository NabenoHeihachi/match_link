from app_profile.models.personality_model import PersonalityModel

class UtilMatching:
    def calculate_matching_score(self, target_user_personality: PersonalityModel, candidate_personality: PersonalityModel) -> float:
        """
        マッチングスコアを計算する  
        :param target_user: ターゲットユーザー
        :param candidate: 候補ユーザー
        :return: マッチングスコア
        """
        try:
            target_personality = target_user_personality
            candidate_personality = candidate_personality

            # Big Five 距離（小さい方が良い）
            big_five_distance = sum([
                abs(target_personality.big_five_extraversion - candidate_personality.big_five_extraversion),
                abs(target_personality.big_five_neuroticism - candidate_personality.big_five_neuroticism),
                abs(target_personality.big_five_openness - candidate_personality.big_five_openness),
                abs(target_personality.big_five_agreeableness - candidate_personality.big_five_agreeableness),
                abs(target_personality.big_five_conscientiousness - candidate_personality.big_five_conscientiousness),
            ])

            # タグ一致率（高い方が良い）
            def calc_tag_score(field):
                t_tags = set(getattr(target_personality, field).values_list('id', flat=True))
                c_tags = set(getattr(candidate_personality, field).values_list('id', flat=True))
                if not t_tags and not c_tags:
                    return 1.0  # 両者空なら一致
                return len(t_tags & c_tags) / len(t_tags | c_tags)

            hobby_score = calc_tag_score('hobby_tags')
            value_score = calc_tag_score('value_tags')
            communication_score = calc_tag_score('communication_tags')

            # スコア計算（例：距離を正規化して減点）
            final_score = (
                (1 / (1 + big_five_distance)) * 0.5 +
                hobby_score * 0.1 +
                value_score * 0.2 +
                communication_score * 0.2
            )

            final_score = round(final_score * 100, 4)  # スコアをパーセンテージに変換
            return final_score
        except:
            return 0