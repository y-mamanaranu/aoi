# Aoi
Aoi is a bot for automating profile channel management on chat servers.
Aoi monitors the profile channel and when a member with a particular role reacts, Aoi grants the role to the user who received the reaction.
It is intended to grant roles to new members with Aoi.

[Add Aoi to Server](https://discord.com/api/oauth2/authorize?client_id=1004329762484916304&permissions=2416126992&scope=bot)

## Config
Aoi needs the environment variables below in the hosted server.
If you are trying to host Aoi yourself, please set them in some way.
If you are a bot user, please skip this section.

|    environ     |             content             |
| -------------- | ------------------------------- |
| `TOKEN`        | Discord Bot Token               |
| `DATABASE_URL` | Database URL of Heroku Postgres |

## Parameters

|   name    |              content              | default |
| --------- | --------------------------------- | ------- |
| prefix    | Prefix of command                 | `;`     |
| #Profile  | Profile channel                   | `None`  |
| #Log      | Log channel                       | `None`  |
| @Freshman | Role to assign to new member      | `None`  |
| @Senior   | Role who can assign to new member | `None`  |


## Commands

|           command           |                            content                             | required Previlage |
| --------------------------- | -------------------------------------------------------------- | ------------------ |
| `/duplicate`                | Delete second or subsequent profile of same user.              | manage_messages    |
| `/clear`                    | Delete profile of leaved member.                               | manage_messages    |
| `/move [<vocie_channel>]`   | Move all member to `vocie_channel`.                            |                    |
| `/profile <user>`           | Show profile of `user`.                                        |                    |
| `/setprofile [<profile>]`   | Change #Profile to `profile`.                                  | administrator      |
| `/limit [<limit>]`          | Change upper limit of voice channel which you join to `limit`. |                    |
| `/setlog [<log>]`           | Change #Log to `log`.                                          | administrator      |
| `/setprefix <prefix>`       | Change prefix to `prefix`.                                     | administrator      |
| `/setfreshman [<freshman>]` | Change @Freshman to `freshman`.                                | manage_roles       |
| `/setsenior [<senior>]`     | Change @Senior to `senior`.                                    | manage_roles       |
| `/split [<vocie_channel>]`  | Split voice channel member and move half to `vocie_channel`.   |                    |
| `/status`                   | Show current config.                                           |                    |

## Generate `requirements.txt`
If you add a new dependency to Aoi, please update `requirements.txt`.

```
poetry export -f requirements.txt --output requirements.txt
```

## See Also
- [dpy\_development\_plans\.md](https://gist.github.com/Rapptz/c4324f17a80c94776832430007ad40e6)
- [Discord Developer Portal — My Applications](https://discord.com/developers/applications)
- [Personal apps \| Heroku](https://dashboard.heroku.com/apps)
- [Discord Botアカウント初期設定ガイド for Developer \- Qiita](https://qiita.com/1ntegrale9/items/cb285053f2fa5d0cccdf)
- [Pythonで実用Discord Bot\(discordpy解説\) \- Qiita](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)
- [discord\.pyでスラッシュコマンド \- discordpy\-japan](https://scrapbox.io/discordpy-japan/discord.py%E3%81%A7%E3%82%B9%E3%83%A9%E3%83%83%E3%82%B7%E3%83%A5%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89)
