# Aoi
Aoi is a bot for automating profile channel management on chat servers.
Aoi monitors the profile channel and when a member with a particular role reacts, Aoi grants the role to the user who received the reaction.
It is intended to grant roles to new members with Aoi.

[Add Aoi to Server](https://discord.com/api/oauth2/authorize?client_id=1004329762484916304&permissions=2416126992&scope=bot)

## Config
Aoi needs the environment variables below in the hosted server.
If you are trying to host Aoi yourself, please set them in some way.
If you are a bot user, please skip this section.

|          environ          |              content               |
| ------------------------- | ---------------------------------- |
| `TOKEN`                   | Discord Bot Token                  |
| `DATABASE_URL`            | Database URL of Heroku Postgres    |
| `TWITTER_CONSUMER_KEY`    | Consumer Key of Twitter            |
| `TWITTER_CONSUMER_SECRET` | Twitter Consumer Secret of Twitter |

## Parameters

|     name      |                 content                 | default |             DB              |          comment          | TODO |
| ------------- | --------------------------------------- | ------- | --------------------------- | ------------------------- | ---- |
| -             |                                         |         | guild_id                    |                           |      |
| prefix        | Prefix of command                       | `;`     | prefix                      |                           |      |
| #Profile      | Profile channel                         | `None`  | profile_id                  |                           |      |
| #Log          | Log channel                             | `None`  | log_id                      |                           |      |
| @Freshman     | Role to assign to new member            | `None`  | freshman_id                 |                           |      |
| @Senior       | Role who can assign to new member       | `None`  | senior_id                   |                           |      |
| :emoji:       | Emoji to assign role                    | `None`  | emoji_id                    | `None` match to any emoji |      |
| #Tenki        | Weather forecast channel                | `None`  | tenki_id                    |                           |      |
| limit?        | Whether activate `/limit`               | `False` | if_limit                    |                           |      |
| adjust?       | Wheter activate `on_voice_state_update` | `False` | if_adjust                   |                           |      |
| move?         |                                         | `False` | if_move                     |                           |      |
| create_voice? |                                         | `False` | if_create_voice             |                           |      |
| create_text?  |                                         | `False` | if_create_text              |                           |      |
| template      |                                         | `None`  | twitter_template            |                           |      |
| -             |                                         | `None`  | twitter_access_token        | Not accsesible            |      |
| -             |                                         | `None`  | twitter_access_token_secret | Not accsesible            |      |

## Commands

|           command            |                            content                             | required previlage |     to disable     | default |  TODO  |
| ---------------------------- | -------------------------------------------------------------- | ------------------ | ------------------ | ------- | ------ |
| `/authtwitter`               |                                                                | administrator      |                    |         |        |
| `/clean`                     | Delete profile of leaved member.                               | manage_messages    | #Profile is `None` | disable |        |
| `/detail`                    |                                                                |                    |                    |         | update |
| `/duplicate`                 | Delete second or subsequent profile of same user.              | manage_messages    | #Profile is `None` | disable |        |
| `/limit [<limit>]`           | Change upper limit of voice channel which you join to `limit`. |                    | limit? is `False`  | disable |        |
| `/move [<vocie_channel>]`    | Move all member to `vocie_channel`.                            |                    | move? is `False`   | disable |        |
| `/profile <user>`            | Show profile of `user`.                                        |                    | #Profile is `None` | disable |        |
| `/random`                    |                                                                |                    |                    |         |        |
| `/rename <name>`             |                                                                |                    |                    |         |        |
| `/set adjust <enable>`       | Change adjust? to `<enable>`                                   | manage_channels    |                    |         |        |
| `/set create_text <enable> ` |                                                                | manage_channels    |                    |         |        |
| `/set create_voice <enable>` |                                                                | manage_channels    |                    |         |        |
| `/set emoji [<emoji>]`       | Change :emoji: to `emoji`.                                     | manage_roles       |                    |         |        |
| `/set freshman [<freshman>]` | Change @Freshman to `freshman`.                                | manage_roles       |                    |         |        |
| `/set limit <enable>`        | Change limit? to `<enable>`                                    | manage_channels    |                    |         |        |
| `/set log [<log>]`           | Change #Log to `log`.                                          | administrator      |                    |         |        |
| `/set move <enable>`         |                                                                | move_members       |                    |         |        |
| `/set prefix <prefix>`       | Change prefix to `prefix`.                                     | administrator      |                    |         |        |
| `/set profile [<profile>]`   | Change #Profile to `profile`.                                  | administrator      |                    |         |        |
| `/set senior [<senior>]`     | Change @Senior to `senior`.                                    | manage_roles       |                    |         |        |
| `/set tenki [<tenki>]`       | Change #Tenki to `tenki`.                                      | administrator      |                    |         |        |
| `/set twitter`               |                                                                | administrator      |                    |         |        |
| `/shuffle [<vocie_channel>]` | Shuffle members with `vocie_channel`.                          |                    | move? is `False`   | disable |        |
| `/split [<vocie_channel>]`   | Split voice channel member and move half to `vocie_channel`.   |                    | move? is `False`   | disable |        |
| `/status`                    | Show current config.                                           |                    |                    |         | update |
| `/tenki`                     | Post weather forecast of tenki.jp.                             |                    |                    |         |        |
| `/tweet`                     |                                                                |                    |                    |         |        |

Commands whose name starts with "/set" change parameters.

## Passive Commands

|        command        |                                             content                                              |                    to disable                    | default | TODO |     |
| --------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------ | ------- | ---- | --- |
| on_raw_reaction_add   | When @Senior adds :emoji: to a message in #Profile, the author of the message receives @Freshman | Any of @Freshman, @Senior and #Profile is `None` | disable |      |     |
| post_tenki            | Run `/tenki` on 5:00 JST                                                                         | #Tenki is `None`                                 | disable |      |     |
| on_voice_state_update | When Bot join/leave vocie channel, increase/decrease the user limit                              | adjust? is `False`                               | disable |      |     |
|                       | Automatically create voice channel and if create_text? create text channel in addition           | create_voice? is `False`                         | disable |      |     |

If you use automatic voice channel creation, please be careful of the name of voice channels.
* `/` is a sign of an automatically created channel.
* `_` is a sign of a channel to ignore.

## Generate `requirements.txt`
If you add a new dependency to Aoi, please update `requirements.txt`.

```
poetry export -f requirements.txt --output requirements.txt
```

```
msgfmt aoi.po -o aoi.mo
git add -f aoi.mo
```

## See Also
- [dpy\_development\_plans\.md](https://gist.github.com/Rapptz/c4324f17a80c94776832430007ad40e6)
- [Discord Developer Portal — My Applications](https://discord.com/developers/applications)
- [Personal apps \| Heroku](https://dashboard.heroku.com/apps)
- [Discord Botアカウント初期設定ガイド for Developer \- Qiita](https://qiita.com/1ntegrale9/items/cb285053f2fa5d0cccdf)
- [Pythonで実用Discord Bot\(discordpy解説\) \- Qiita](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)
- [discord\.pyでスラッシュコマンド \- discordpy\-japan](https://scrapbox.io/discordpy-japan/discord.py%E3%81%A7%E3%82%B9%E3%83%A9%E3%83%83%E3%82%B7%E3%83%A5%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89)
