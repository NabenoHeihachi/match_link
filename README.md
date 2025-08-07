# MATCH LINK

## １）概要

- - 本システムは、企業における若年層社員の定着率向上と、上司とのミスマッチによる早期離職防止を目的としたシステムです。社員が自己理解を深め、性格・趣味・価値観・コミュニケーションスタイルの観点から相性の良い上司及び部下をマッチングする仕組みを提供します。

## ２）初回セットアップ

- ダウンロード後、以下を実行

```
cd match_link
```

```
cp .env.example .env
```

```
docker compose build
```

```
docker compose up -d
```

```
docker compose exec web python manage.py makemigrations
```

```
docker compose exec web python manage.py migrate
```

```
docker compose exec web python manage.py custom_insert_init_data
```

## ３）ローカルサーバー

#### a.開始時

```
docker compose up -d
```

```
docker compose up -d --remove-orphans 
```

#### b.終了時

```
docker compose stop
```

```
docker compose down
```

```
docker compose down -v
```
### c.再起動
```
docker compose stop && docker compose up -d
```

#### d.再作成
```
docker compose down -v && docker compose up -d && docker compose exec web python manage.py makemigrations && docker compose exec web python manage.py migrate && docker compose exec web python manage.py custom_insert_init_data_account && docker compose exec web python manage.py custom_insert_init_data_profile && docker compose stop && docker compose up -d
```

#### e.アカウントロックのリセット
```
docker compose exec web python manage.py axes_reset 
```


## ４）初期管理アカウント

パス：

```
/system-manager/admin-site/
```

アカウントID：（組織ID＋.env[INIT_ACCOUNT_ID]）

```
100000001
```

パスワード：（.env[INIT_PASSWORD]）

```
Password@1234
```
