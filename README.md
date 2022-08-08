# Aoi
Aoi is a bot for automating profile channel management on chat servers.
Aoi monitors the profile channel and when a member with a particular role reacts, Aoi grants the role to the user who received the reaction.
It is intended to grant roles to new members with Aoi.

## Config
Aoi needs the environment variables below in the hosted server.
If you are trying to host Aoi yourself, please set them in some way.
If you are a bot user, please skip this section.

|    environ     |             content             |
| -------------- | ------------------------------- |
| `TOKEN`        | Discord Bot Token               |
| `DATABASE_URL` | Database URL of Heroku Postgres |

## Commands

|           command           |                             content                              |
| --------------------------- | ---------------------------------------------------------------- |
| `;adjustment`               | Delete message from duplicate message in profile channel.        |
| `;eliminate`                | Elminate message from leaved member in profile channel.          |
| `;guild`                    | Return name and id of guild.                                     |
| `;help`                     | Show help.                                                       |
| `;roles`                    | List name and id of roles.                                       |
| `;setadmin <admin_role_id>` | Change ID of admin role to `admin_role_id`. Default is `None`.   |
| `;setchannel <channel_id>`  | Change ID of profile channel to `channel_id`. Default is `None`. |
| `;setprefix <prefix>`       | Change prefix to `prefix`. Default prefix is `;`.                |
| `;setrole <role_id>`        | Change ID of role to assign to `role_id`. Default is `None`.     |
| `;status`                   | Show current config.                                             |
| `;text_channels`            | List name and id of text channels.                               |


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
