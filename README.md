# Aoi
Aoi monitors a particular channel and when a member with a particular role reacts, Aoi grants the role to the user who received the reaction.

## Config
Aoi needs environment variables below.

|     environ      |                  content                  |
| ---------------- | ----------------------------------------- |
| `AOI_TOKEN`      | Discord Bot Token                         |
| `AOI_ROLE_ID`    | ID of role which Aoi grant                |
| `AOI_CHANNEL_ID` | ID of channel which Aoi look for reaction |

## Commands

|     command      |        content         |
| ---------------- | ---------------------- |
| `;roles`         | List all roles         |
| `;text_channels` | List all text channels |


## Generate `requirements.txt`
```
poetry export -f requirements.txt --output requirements.txt
```

## See Also
- [Discord Developer Portal — My Applications](https://discord.com/developers/applications)
- [Discord Botアカウント初期設定ガイド for Developer \- Qiita](https://qiita.com/1ntegrale9/items/cb285053f2fa5d0cccdf)
- [Pythonで実用Discord Bot\(discordpy解説\) \- Qiita](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)
- [discord\.pyでスラッシュコマンド \- discordpy\-japan](https://scrapbox.io/discordpy-japan/discord.py%E3%81%A7%E3%82%B9%E3%83%A9%E3%83%83%E3%82%B7%E3%83%A5%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89)