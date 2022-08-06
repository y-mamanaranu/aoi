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
